import React from 'react';
import styles from './FeaturesShowcase.module.css';

interface Feature {
  title: string;
  description: string;
  icon: string;
}

const features: Feature[] = [
  {
    title: 'AI Teaching Assistant',
    description: 'Ask questions about any topic and get intelligent, context-aware answers powered by RAG technology.',
    icon: '🤖',
  },
  {
    title: '16 Comprehensive Chapters',
    description: 'Carefully structured curriculum spanning from Python fundamentals to advanced humanoid robotics control.',
    icon: '📚',
  },
  {
    title: 'Interactive Learning',
    description: 'Highlight text, explore concepts, and receive personalized learning recommendations based on your progress.',
    icon: '✨',
  },
  {
    title: 'Track Progress',
    description: 'Monitor your learning journey with session history and progress tracking across all 4 modules.',
    icon: '📊',
  },
  {
    title: 'Hands-on Examples',
    description: 'Learn with real-world code examples, simulations, and practical exercises throughout the textbook.',
    icon: '💻',
  },
  {
    title: 'Expert Guidance',
    description: 'Access curated resources, best practices, and expert insights from robotics professionals.',
    icon: '🎯',
  },
];

export const FeaturesShowcase: React.FC = () => {
  return (
    <section className={styles.section}>
      <div className={styles.container}>
        <h2 className={styles.title}>Why Choose This Living Textbook?</h2>
        <p className={styles.subtitle}>
          A complete learning ecosystem designed for modern roboticists
        </p>

        <div className={styles.grid}>
          {features.map((feature, index) => (
            <div key={index} className={styles.featureCard}>
              <div className={styles.iconWrapper}>
                <span className={styles.icon}>{feature.icon}</span>
              </div>
              <h3 className={styles.featureTitle}>{feature.title}</h3>
              <p className={styles.featureDescription}>{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};
