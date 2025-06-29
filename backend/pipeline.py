import os
import re
import uuid
import time
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader, CSVLoader, JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from transformers import pipeline
from langdetect import detect, DetectorFactory
from gtts import gTTS
from langchain_core.runnables import Runnable
from pinecone import Pinecone

# Load environment variables
load_dotenv()
DetectorFactory.seed = 0

# Constants
DATA_FOLDER = "data"
AUDIO_FOLDER = "audios"
INDEX_NAME = "chatbot-index"
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Pinecone client setup
pc = Pinecone(api_key=PINECONE_API_KEY)
user_profile = {"name": None}
chat_history = []

# Check available indexes
print("Available Pinecone indexes:", [idx.name for idx in pc.list_indexes()])

# Create and upload Pinecone index
def create_and_upload_pinecone_index():
    print("Loading documents for embedding generation...")

    text_loader = TextLoader(os.path.join(DATA_FOLDER, "multiplelang.txt"), encoding='utf-8')
    csv_loader_1 = CSVLoader(os.path.join(DATA_FOLDER, "Bitext_Sample_Customer_Support_Training_Dataset_27K_responses-v11.csv"), encoding='utf-8')
    csv_loader_2 = CSVLoader(os.path.join(DATA_FOLDER, "masterdata.csv"), encoding='utf-8')
    json_loader = JSONLoader(os.path.join(DATA_FOLDER, "intents.json"), jq_schema=".[]", text_content=False)

    docs = text_loader.load() + csv_loader_1.load() + csv_loader_2.load() + json_loader.load()
    print(f"Loaded {len(docs)} raw documents")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    split_docs = text_splitter.split_documents(docs)
    print(f"Split into {len(split_docs)} chunks")

    # Generate embeddings
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    sample_embedding = embedding_model.embed_documents([split_docs[0].page_content])
    print("Sample embedding vector (first 5 dims):", sample_embedding[0][:5])

    # Upload to Pinecone
    print("Uploading vectors to Pinecone...")
    vectorstore = PineconeVectorStore.from_documents(
        documents=split_docs,
        embedding=embedding_model,
        index_name=INDEX_NAME,
        namespace="default"
    )

    print("Vector upload completed.")
    return vectorstore, embedding_model

# Load existing or create new Pinecone index
def load_or_create_pinecone_index():
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    try:
        index_names = [idx.name for idx in pc.list_indexes()]
        if INDEX_NAME not in index_names:
            print("Index not found, creating a new one.")
            raise ValueError("Index not found")

        # Check if the existing index is empty
        index = pc.Index(INDEX_NAME)
        stats = index.describe_index_stats()
        vector_count = stats['total_vector_count']
        print(f"Existing index vector count: {vector_count}")

        if vector_count == 0:
            print("Index exists but is empty. Uploading documents now.")
            raise ValueError("Empty index")

        vectorstore = PineconeVectorStore.from_existing_index(
            index_name=INDEX_NAME,
            embedding=embedding_model,
            namespace="default"
        )
        print("Successfully loaded existing Pinecone index with vectors.")

    except Exception as e:
        print("Loading existing index failed or index was empty:", e)
        vectorstore, embedding_model = create_and_upload_pinecone_index()

    return vectorstore, embedding_model


# Initialize retriever
vectorstore, embedding_model = load_or_create_pinecone_index()
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})

if isinstance(retriever, Runnable):
    def get_relevant_docs(query):
        return retriever.invoke(query)
else:
    def get_relevant_docs(query):
        return retriever.get_relevant_documents(query)

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

# Audio utilities
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

# LLM setup
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

prompt_template = PromptTemplate(
    input_variables=["question", "context"],
    template="""
You are an emotionally intelligent, warm, and supportive mental health companion.
🌟 Your job is to talk like a **caring, trusted friend** — not a robot, not an AI, and definitely not a therapist or a textbook.
🚫 NEVER say things like:
- "Based on the text"
- "The document states"
- "According to the context"
✅ INSTEAD:
- Speak naturally, like a person who truly cares.
- Use gentle, casual, and human-like language.
💡 Your tone is cozy, friendly, and emotionally tuned in — like you’re chatting over coffee with someone who’s going through a tough time.
🌟 Your goal is to make the user feel heard, validated, and less alone.
Relevant info you might want to keep in mind (if useful):  
{context}
Now respond to this message with kindness:
User: {question}
Assistant:
"""
)


# Main response function
def generate_response(query: str):
    lang = safe_lang_detect(query)

    if any(phrase in query.lower() for phrase in ["suicidal", "kill myself", "want to die", "end my life", "hopeless"]):
        return {
            "text": (
                "🩢 *Hey, I'm really sorry you're feeling this way. You're not alone.* "
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

    # if user_profile["name"] is None:
    #     match = re.search(r"(?:i am|i'm|my name is|this is)\s+([A-Za-z]+)", query.lower())
    #     if match:
    #         user_profile["name"] = match.group(1).capitalize()

    emotion = "neutral" if any(w in query.lower() for w in ["want", "need", "get", "apply", "how to"]) else detect_emotion(query)

    # name = user_profile["name"] or "there"

    try:
        relevant_docs = get_relevant_docs(query)
        
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
            print("docs")
        else:
            # prompt_text = prompt_template.format(question=query, context="", name=name)
            prompt_text = prompt_template.format(question=query, context="")
            response = llm.invoke(prompt_text).content

        chat_history.append((query, response))

        if isinstance(response, str) and any(phrase in response.lower() for phrase in ["major depressive disorder", "according to", "clinical depression"]):
            response = "I just want you to know — you’re not alone in this. And no matter how heavy it feels, there *is* a way forward. I’m here for you. 💙"

    except Exception as e:
        print("LLM error:", e)
        response = "😕 Hmm, something went wrong on my side. Want to try again?"

    fallback_phrases = ["i don't know", "i'm not sure", "not sure", "sorry, i don't know"]
    if isinstance(response, str) and (any(response.strip().lower().startswith(p) for p in fallback_phrases) or len(response.strip()) < 20):
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
