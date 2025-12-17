/**
 * Docusaurus Root wrapper component.
 * Wraps the entire app to inject global components like the RAG Chatbot.
 */

import React from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import ChatkitChatbot from '@site/src/components/Chatkit-chatbot';

export default function Root({ children }) {
  return (
    <>
      {children}
      <BrowserOnly>
        {() => <ChatkitChatbot />}
      </BrowserOnly>
    </>
  );
}
