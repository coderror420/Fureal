import os
import re
import uuid
import time
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader, CSVLoader, JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from transformers import pipeline
from langdetect import detect, DetectorFactory
from gtts import gTTS

load_dotenv()
DetectorFactory.seed = 0

# Constants
DATA_FOLDER = "data"
INDEX_FOLDER = "vectorstore"
AUDIO_FOLDER = "audios"

user_profile = {"name": None}
chat_history = []

# Generate embeddings and FAISS index ONLY IF missing
def generate_and_save_faiss_index(data_folder=DATA_FOLDER, index_folder=INDEX_FOLDER):
    print("Loading documents for embedding generation...")
    text_loader = TextLoader(os.path.join(data_folder, "multiplelang.txt"), encoding='utf-8')
    csv_loader_1 = CSVLoader(os.path.join(data_folder, "Bitext_Sample_Customer_Support_Training_Dataset_27K_responses-v11.csv"), encoding='utf-8')
    csv_loader_2 = CSVLoader(os.path.join(data_folder, "masterdata.csv"), encoding='utf-8')
    json_loader = JSONLoader(os.path.join(data_folder, "intents.json"), jq_schema=".[]", text_content=False)

    docs = text_loader.load() + csv_loader_1.load() + csv_loader_2.load() + json_loader.load()
    print(f"Loaded {len(docs)} documents")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    split_docs = text_splitter.split_documents(docs)
    print(f"Split into {len(split_docs)} document chunks")

    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    print("Generating embeddings and building FAISS index...")
    vectorstore = FAISS.from_documents(documents=split_docs, embedding=embedding_model)

    os.makedirs(index_folder, exist_ok=True)
    vectorstore.save_local(index_folder)
    print("FAISS index saved locally.")

    return vectorstore, embedding_model

def load_or_create_faiss_index(index_folder=INDEX_FOLDER, data_folder=DATA_FOLDER):
    index_path = os.path.join(index_folder, "index.faiss")
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    if os.path.exists(index_path):
        print("✅ FAISS index found locally, loading...")
        vectorstore = FAISS.load_local(index_folder, embedding_model, allow_dangerous_deserialization=True)
    else:
        print("❌ FAISS index NOT found, generating embeddings and index now...")
        vectorstore, embedding_model = generate_and_save_faiss_index(data_folder=data_folder, index_folder=index_folder)

    return vectorstore, embedding_model

# Language detection
def safe_lang_detect(text):
    try:
        lang = detect(text)
        if lang in ["en", "hi"]:
            return lang
        if len(text.split()) <= 6:
            return "en"
    except:
        pass
    return "en"

# Emotion detection
emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=1)

def detect_emotion(text: str) -> str:
    try:
        result = emotion_classifier(text)
        return result[0][0]["label"]
    except Exception as e:
        print("Emotion detection failed:", e)
        return "neutral"

# Audio utils
def cleanup_old_audios(folder=AUDIO_FOLDER, max_age_minutes=30):
    current_time = time.time()
    if not os.path.exists(folder):
        return
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        if os.path.isfile(path):
            age_minutes = (current_time - os.path.getmtime(path)) / 60
            if age_minutes > max_age_minutes:
                try:
                    os.remove(path)
                except:
                    pass

def generate_audio(text, lang="en", output_folder=AUDIO_FOLDER):
    os.makedirs(output_folder, exist_ok=True)
    cleanup_old_audios(output_folder)
    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(output_folder, filename)
    tts = gTTS(text=text, lang=lang)
    tts.save(filepath)
    return filepath

# Load or generate FAISS index once on start
vectorstore, embedding_model = load_or_create_faiss_index()
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# Prompt template
base_prompt = """
You are an emotionally intelligent, warm, and supportive mental health companion.
✨ Your job is to talk like a **caring, trusted friend** — not a robot, not an AI, and definitely not a therapist or a textbook.
🚫 NEVER say things like:
- "Based on the text"
- "The document states"
- "You might be experiencing"
- "According to the context"
- "As an AI"
- "The source says"
✅ INSTEAD:
- Speak naturally, like a person who truly cares.
- Use gentle, casual, and human-like language.
- Show you understand the user’s feelings.
- Give comforting, supportive replies — NOT medical definitions.
💡 Your tone is cozy, friendly, and emotionally tuned in — like you’re chatting over coffee with someone who’s going through a tough time.
🎯 Your goal is to make {name} feel heard, validated, and less alone.
Relevant info you might want to keep in mind (if useful):  
{context}
Now respond to this message with kindness:
User: {question}
Assistant:
"""
prompt_template = PromptTemplate(input_variables=["question", "context"], template=base_prompt)

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Main chat response function
def generate_response(query: str):
    lang = safe_lang_detect(query)

    # Suicide / crisis override response
    if any(phrase in query.lower() for phrase in ["suicidal", "kill myself", "want to die", "end my life", "hopeless"]):
        return {
            "text": (
                "🥲 *Hey, I'm really sorry you're feeling this way. You're not alone.* "
                "It takes courage to talk about it, and I'm here for you. Please try reaching out to someone you trust, "
                "or connect with a mental health professional.\n\n"
                "📞 *In India, you can contact iCall (+91-9152987821) or AASRA (+91-9820466726).* "
                "They’re amazing and ready to listen—anytime.\n\n"
                "*Big hug from my side.* ❤️ *You matter more than you know.*"
            )
        }

    if lang not in ["en", "hi"]:
        return {
            "text": "⚠️ Sorry, I can only chat in English or Hindi right now. Let's stick to those so I can help you best!"
        }

    # Capture user name if unknown
    if user_profile["name"] is None:
        match = re.search(r"(?:i am|i'm|my name is|this is)\s+([A-Za-z]+)", query.lower())
        if match:
            user_profile["name"] = match.group(1).capitalize()

    # Detect emotion heuristically
    if any(w in query.lower() for w in ["want", "need", "get", "apply", "how to"]):
        emotion = "neutral"
    else:
        emotion = detect_emotion(query)

    name = user_profile["name"] or "there"

    try:
        relevant_docs = retriever.get_relevant_documents(query)
        context = "\n\n".join(doc.page_content for doc in relevant_docs) if relevant_docs else ""

        if context.strip():
            qa_chain = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=retriever,
                memory=None,
                combine_docs_chain_kwargs={"prompt": prompt_template},
            )
            result = qa_chain.invoke({"question": query, "context": context, "chat_history": chat_history})
            response = result["answer"]
        else:
            prompt_text = base_prompt.replace("{name}", name).replace("{context}", "").format(question=query)
            response = llm.invoke(prompt_text)

        chat_history.append((query, response))

        if any(phrase in response.lower() for phrase in ["major depressive disorder", "according to", "clinical depression"]):
            response = "I just want you to know — you’re not alone in this. And no matter how heavy it feels, there *is* a way forward. I’m here for you. 💙"

    except Exception as e:
        print("LLM error:", e)
        response = "😕 Hmm, something went wrong on my side. Want to try again?"

    fallback_phrases = ["i don't know", "i'm not sure", "not sure", "sorry, i don't know"]
    if any(response.strip().lower().startswith(p) for p in fallback_phrases) or len(response.strip()) < 20:
        response = "*Hmm... I'm not totally sure, but I'm still here to talk if you’d like!* 💬"

    emotion_prefix = {
        "anger": "😤 *I hear your frustration.* Let's sort this out together. ",
        "sadness": "💙 *Aww, that sounds tough.* You're not alone. ",
        "joy": "😊 *Yay! That's awesome!* ",
        "fear": "😟 *It's okay to be scared sometimes.* I'm right here with you. ",
        "neutral": "🙂 ",
    }

    full_response = emotion_prefix.get(emotion.lower(), "") + response.strip()
    audio_path = generate_audio(full_response, lang=lang)

    return {
        "text": full_response,
        "audio": audio_path
    }
