/**
 * Premium RAG Chatbot Component with ChatKit React
 * Technical Precision + Futuristic Elegance Design
 * Features: Selected-text questioning, conversation history, glass morphism UI
 */
import React, { useEffect, useState, useCallback, useRef } from 'react';
import { useChatKit, ChatKit } from '@openai/chatkit-react';
import styles from './styles.module.css';

// SVG Icons for premium UI
const ChatIcon = () => (
  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 13.5997 2.37562 15.1116 3.04346 16.4525C3.22094 16.8088 3.28001 17.2161 3.17712 17.6006L2.58151 19.8267C2.32295 20.793 3.20701 21.677 4.17335 21.4185L6.39939 20.8229C6.78393 20.72 7.19121 20.7791 7.54753 20.9565C8.88837 21.6244 10.4003 22 12 22Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

const SparkleIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 2L13.5 8.5L20 10L13.5 11.5L12 18L10.5 11.5L4 10L10.5 8.5L12 2Z" fill="currentColor" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M19 3L19.5 5.5L22 6L19.5 6.5L19 9L18.5 6.5L16 6L18.5 5.5L19 3Z" fill="currentColor"/>
  </svg>
);

const CloseIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Generate or retrieve session ID from localStorage
const getSessionId = () => {
  let sessionId = localStorage.getItem('chatkit_session_id');
  if (!sessionId) {
    sessionId = `session_${Date.now()}_${Math.random().toString(36).substring(7)}`;
    localStorage.setItem('chatkit_session_id', sessionId);
  }
  return sessionId;
};

const ChatkitChatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const [showAskButton, setShowAskButton] = useState(false);
  const [buttonPosition, setButtonPosition] = useState({ x: 0, y: 0 });
  const [sessionId] = useState(getSessionId);

  // Use ref to always get current selectedText value in customFetch
  const selectedTextRef = useRef('');

  // Update ref whenever selectedText changes
  useEffect(() => {
    selectedTextRef.current = selectedText;
    console.log('📝 selectedText updated:', selectedText);
  }, [selectedText]);

  // Custom fetch function to pass session_id and selected_text as headers
  // Using ref ensures we always get the CURRENT selectedText value
  const customFetch = useCallback(
    async (url, options = {}) => {
      const currentSelectedText = selectedTextRef.current;

      console.log('🚀 customFetch called');
      console.log('📝 selectedText from ref:', currentSelectedText);
      console.log('🆔 sessionId:', sessionId);

      const headers = {
        ...options.headers,
        'X-Session-Id': sessionId,
        'X-Selected-Text': currentSelectedText || '',
      };

      console.log('📤 Headers being sent:', headers);

      return fetch(url, {
        ...options,
        headers,
      });
    },
    [sessionId]  // Only depends on sessionId now, not selectedText
  );

  // Auto-detect backend URL based on environment
  const getBackendUrl = () => {
    // SSR safety check
    if (typeof window === 'undefined') {
      return 'https://alishba20-05-robotics-book.hf.space/chatkit';
    }

    // Check if running locally
    if (window.location.hostname === 'localhost') {
      return 'http://localhost:8001/chatkit';
    }

    // Production: Use HF Space URL
    return 'https://alishba20-05-robotics-book.hf.space/chatkit';
  };

  // Get domain key with SSR safety
  const getDomainKey = () => {
    if (typeof window === 'undefined') return 'production';
    return window.location.hostname === 'localhost' ? 'local-dev' : 'production';
  };

  // Initialize ChatKit with custom backend configuration
  const backendUrl = getBackendUrl();
  const domainKey = getDomainKey();

  // Debug logging
  console.log('🔧 ChatKit Configuration:', {
    backendUrl,
    domainKey,
    sessionId,
    hostname: typeof window !== 'undefined' ? window.location.hostname : 'SSR'
  });

  const { control } = useChatKit({
    api: {
      url: backendUrl,
      domainKey: domainKey,
      fetch: customFetch,
    },
    startScreen: {
      greeting: 'What can I help you today with?',
      prompts: [
        {
          label: 'Explain inverse kinematics',
          prompt: 'What is inverse kinematics in humanoid robotics?',
        },
        {
          label: 'Sensor systems overview',
          prompt: 'Tell me about sensor systems in humanoid robots',
        },
        {
          label: 'Actuators and motors',
          prompt: 'How do actuators work in humanoid robots?',
        },
      ],
    },
    composer: {
      placeholder: selectedText
        ? 'Ask about the selected text...'
        : 'Ask me anything about humanoid robotics...',
    },
    header: {
      enabled: false, // We have custom header
    },
    history: {
      enabled: true,
      showDelete: false,
      showRename: false,
    },
    threadItemActions: {
      feedback: false,
      retry: true,
    },
  });

  // Handle text selection
  useEffect(() => {
    const handleTextSelection = () => {
      const selection = window.getSelection();
      const text = selection?.toString().trim();

      if (text && text.length > 0 && text.length < 2000) {
        setSelectedText(text);

        // Get selection position for button placement
        const range = selection.getRangeAt(0);
        const rect = range.getBoundingClientRect();

        setButtonPosition({
          x: rect.left + (rect.width / 2),
          y: rect.bottom + window.scrollY + 10,
        });

        setShowAskButton(true);
      } else {
        setShowAskButton(false);
      }
    };

    document.addEventListener('mouseup', handleTextSelection);
    document.addEventListener('touchend', handleTextSelection);

    return () => {
      document.removeEventListener('mouseup', handleTextSelection);
      document.removeEventListener('touchend', handleTextSelection);
    };
  }, []);

  // Handle "Ask about this" button click
  const handleAskAboutSelection = () => {
    setIsOpen(true);
    setShowAskButton(false);
  };

  // Clear selected text
  const clearSelectedText = () => {
    setSelectedText('');
  };

  // Toggle chatbot panel
  const toggleChat = () => {
    setIsOpen(!isOpen);
    if (!isOpen) {
      setShowAskButton(false);
    }
  };

  return (
    <>
      {/* Floating "Ask about this" button for selected text */}
      {showAskButton && !isOpen && (
        <button
          className={styles.askButton}
          style={{
            left: `${buttonPosition.x}px`,
            top: `${buttonPosition.y}px`,
          }}
          onClick={handleAskAboutSelection}
        >
          <SparkleIcon /> Ask about this
        </button>
      )}

      {/* Floating chatbot icon */}
      {!isOpen && (
        <button
          className={styles.floatingIcon}
          onClick={toggleChat}
          aria-label="Open AI Assistant"
          title="Open AI Assistant"
        >
          <ChatIcon />
        </button>
      )}

      {/* Chat panel - Always mounted, visibility controlled by CSS */}
      <div className={styles.chatPanel} style={{ display: isOpen ? 'flex' : 'none' }}>
        {/* Premium header with gradient title and close button */}
        <div className={styles.chatHeader}>
          <h3 className={styles.chatTitle}>Humanoid Robotics Assistant</h3>
          <button
            className={styles.closeButton}
            onClick={toggleChat}
            aria-label="Close chatbot"
            title="Close"
          >
            <CloseIcon />
          </button>
        </div>

        {/* Selected text context display */}
        {selectedText && (
          <div className={styles.selectedTextBox}>
            <div className={styles.selectedTextHeader}>
              <span className={styles.selectedTextLabel}>Selected text:</span>
              <button
                className={styles.clearTextButton}
                onClick={clearSelectedText}
                aria-label="Clear selected text"
              >
                Clear
              </button>
            </div>
            <p className={styles.selectedTextContent}>
              "{selectedText.substring(0, 200)}
              {selectedText.length > 200 ? '...' : ''}"
            </p>
          </div>
        )}

        {/* ChatKit React Component - Always mounted for persistence */}
        <div className={styles.chatContent}>
          <ChatKit control={control} />
        </div>
      </div>
    </>
  );
};

export default ChatkitChatbot;
