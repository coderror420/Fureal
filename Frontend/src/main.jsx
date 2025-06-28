import React from "react"
import { StrictMode } from 'react'
import ReactDOM from "react-dom/client";
import { createRoot } from 'react-dom/client'
import { createBrowserRouter, RouterProvider, Outlet } from "react-router-dom";
import { SignIn, SignUp, RedirectToSignIn, SignedIn, SignedOut } from "@clerk/clerk-react";
import Cover from "./components/Cover.jsx"
import About from "./components/About.jsx"
import Header from "./components/Header.jsx";
import ChatWindow from "./components/chatwindow.jsx";
import FAQ from "./components/Faq.jsx";
import ChatLayout from "./components/ChatLayout.jsx";
import Footer from "./components/Footer.jsx";


// eslint-disable-next-line react-refresh/only-export-components
const AppLayout = ()=>{
  return (
  <StrictMode>
     {/* <ClerkProvider publishableKey={PUBLISHABLE_KEY} afterSignOutUrl="/"> */}
     <div className="">
      <Header/>
      <Outlet/>
     </div>
     
     {/* </ClerkProvider> */}
  </StrictMode>
  );
}

const AppRouter = createBrowserRouter([
  {
    path: "/",
    element: <AppLayout />,
    children: [
      {
        path: "/",
        element: <div>
  <Header />
  <Cover />
  <div id="about"><About /></div>
  <div id="faq"><FAQ /></div>
  <Footer/>
  
</div>,
      },
      {
        path: "/home",
        element: <Cover />,
      },
      {
        path: "/about",
        element: <About />,
      },
      {
        path: "/chat",
        element: <ChatLayout />,
      },
      {
        path: "/faq",
        element: <FAQ />,
      },
    ],
  },
]);
createRoot(document.getElementById('root')).render(
  <RouterProvider router={AppRouter} />
)
