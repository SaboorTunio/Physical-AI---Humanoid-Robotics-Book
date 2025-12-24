import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import styles from './ChatWidget.module.css';

export interface ChatWidgetProps {
  chapterTitle?: string;
  chapterNumber?: number;
}

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: string[];
}

export const ChatWidget: React.FC<ChatWidgetProps> = ({
  chapterTitle = 'Current Chapter',
  chapterNumber = 0,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [contextText, setContextText] = useState('');

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Send request to backend chat endpoint
      const response = await axios.post(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/chat`, {
        query: input,
        context: contextText,
      });

      const { answer, sources } = response.data;

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: answer,
        sources: sources || [],
      };

      setMessages((prev) => [...prev, assistantMessage]);
      setContextText(''); // Clear context after sending
    } catch (error) {
      console.error('Error sending message:', error);

      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error while processing your request. Please try again.',
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleHighlightedText = () => {
    const selection = window.getSelection();
    const selectedText = selection?.toString().trim();

    if (selectedText && selectedText.length > 0) {
      setContextText(selectedText);
      setInput(`Can you explain this: "${selectedText}"`);
      setIsOpen(true);
    }
  };

  useEffect(() => {
    document.addEventListener('mouseup', handleHighlightedText);
    return () => {
      document.removeEventListener('mouseup', handleHighlightedText);
    };
  }, []);

  const clearChat = () => {
    setMessages([]);
  };

  return (
    <>
      {/* Floating button */}
      {!isOpen && (
        <button
          className={styles.floatingButton}
          onClick={() => setIsOpen(true)}
          title="Ask AI Teaching Assistant"
        >
          <span className={styles.icon}>🤖</span>
        </button>
      )}

      {/* Chat widget */}
      {isOpen && (
        <div className={styles.widget}>
          <div className={styles.header}>
            <h3 className={styles.title}>AI Teaching Assistant</h3>
            <div className={styles.headerActions}>
              <button
                className={styles.clearButton}
                onClick={clearChat}
                title="Clear chat"
              >
                🗑️
              </button>
              <button
                className={styles.closeButton}
                onClick={() => setIsOpen(false)}
                title="Close"
              >
                ✕
              </button>
            </div>
          </div>

          <div className={styles.messages}>
            {messages.length === 0 && (
              <div className={styles.welcome}>
                <div className={styles.welcomeIcon}>🤖</div>
                <h4>Hello! I'm your AI Teaching Assistant</h4>
                <p>
                  I'm here to help you understand the content from <strong>{chapterTitle}</strong>.
                </p>
                <p className={styles.tips}>
                  <strong>💡 Tips:</strong>
                </p>
                <ul>
                  <li>Highlight any text and ask me about it</li>
                  <li>Ask questions about concepts you find confusing</li>
                  <li>I'll provide answers grounded in the textbook</li>
                </ul>
              </div>
            )}

            {messages.map((message) => (
              <div
                key={message.id}
                className={`${styles.message} ${styles[message.role]}`}
              >
                <div className={styles.messageContent}>
                  <p>{message.content}</p>
                  {message.sources && message.sources.length > 0 && (
                    <div className={styles.sources}>
                      <strong>Sources:</strong>
                      <div className={styles.sourceList}>
                        {message.sources.map((source, idx) => (
                          <span key={idx} className={styles.source}>
                            {source}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ))}

            {isLoading && (
              <div className={`${styles.message} ${styles.assistant}`}>
                <div className={styles.messageContent}>
                  <div className={styles.typing}>
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {contextText && (
            <div className={styles.contextBanner}>
              <span className={styles.contextText}>Context: "{contextText.substring(0, 50)}..."</span>
              <button
                className={styles.clearContext}
                onClick={() => setContextText('')}
                title="Clear context"
              >
                ✕
              </button>
            </div>
          )}

          <form className={styles.inputForm} onSubmit={handleSendMessage}>
            <input
              type="text"
              className={styles.input}
              placeholder="Ask me anything about this chapter..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={isLoading}
            />
            <button
              type="submit"
              className={styles.sendButton}
              disabled={isLoading || !input.trim()}
              title="Send message"
            >
              {isLoading ? '...' : '→'}
            </button>
          </form>
        </div>
      )}
    </>
  );
};