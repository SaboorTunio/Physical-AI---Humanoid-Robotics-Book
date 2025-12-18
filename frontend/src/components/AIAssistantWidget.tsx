import React, { useState, useRef, useEffect } from 'react';
import styles from './AIAssistantWidget.module.css';

export interface AIAssistantWidgetProps {
  chapterTitle: string;
  chapterNumber: number;
}

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: string[];
}

export const AIAssistantWidget: React.FC<AIAssistantWidgetProps> = ({
  chapterTitle,
  chapterNumber,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

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

    // Simulate API call to backend
    setTimeout(() => {
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `I'm the AI Teaching Assistant for this course. I'm here to help you understand "${chapterTitle}" better. You asked: "${input}"\n\nIn a real implementation, I would connect to the RAG backend to provide context-aware answers based on the textbook content.\n\nTo integrate the real AI assistant, connect this widget to your API endpoint at /api/chat.`,
        sources: ['Chapter ' + chapterNumber, 'Course Materials'],
      };
      setMessages((prev) => [...prev, assistantMessage]);
      setIsLoading(false);
    }, 1000);
  };

  const handleHighlightedText = () => {
    const selectedText = window.getSelection()?.toString();
    if (selectedText) {
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

  return (
    <>
      {/* Floating button */}
      {!isOpen && (
        <button
          className={styles.floatingButton}
          onClick={() => setIsOpen(true)}
          title="Ask AI Assistant"
        >
          <span className={styles.icon}>🤖</span>
        </button>
      )}

      {/* Widget */}
      {isOpen && (
        <div className={styles.widget}>
          <div className={styles.header}>
            <h3 className={styles.title}>AI Teaching Assistant</h3>
            <button
              className={styles.closeButton}
              onClick={() => setIsOpen(false)}
              title="Close"
            >
              ✕
            </button>
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
              <div key={message.id} className={`${styles.message} ${styles[message.role]}`}>
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
