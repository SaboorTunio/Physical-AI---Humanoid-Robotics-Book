import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import styles from './index.module.css';

function HomepageHeader() {
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className={styles.heroTitle}>
          Physical AI & Humanoid Robotics Textbook
        </Heading>
        <Heading as="h2" className={styles.heroSubheading}>
          Interactive Learning with AI Teaching Assistant
        </Heading>
        <p className={styles.heroSubtitle}>
          An interactive, AI-powered learning platform that combines comprehensive curriculum on Physical AI and Humanoid Robotics with an intelligent Teaching Assistant powered by advanced RAG (Retrieval-Augmented Generation) technology.
        </p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro"
          >
            Start Reading →
          </Link>
        </div>
      </div>
    </header>
  );
}

interface ModuleItem {
  title: string;
  icon: string;
  description: string;
  chapters: number;
  href: string;
  color: string;
}

const ModulesList: ModuleItem[] = [
  {
    title: 'Module 1: Foundations',
    icon: '🏗️',
    description: 'Master Python programming, simulation basics, essential mathematics, and robotics development tools',
    chapters: 4,
    href: '/docs/module-1/chapter-1-python-intro',
    color: 'blue',
  },
  {
    title: 'Module 2: The Body',
    icon: '🤖',
    description: 'Explore sensors, actuators, URDF modeling, and forward/inverse kinematics fundamentals',
    chapters: 4,
    href: '/docs/module-2/chapter-5-sensors-overview',
    color: 'emerald',
  },
  {
    title: 'Module 3: The Brain',
    icon: '🧠',
    description: 'Learn computer vision, PyTorch deep learning, reinforcement learning, and neural network architectures',
    chapters: 4,
    href: '/docs/module-3/chapter-9-computer-vision',
    color: 'purple',
  },
  {
    title: 'Module 4: Humanoid Control',
    icon: '🚀',
    description: 'Build advanced systems for locomotion, manipulation, agentic behaviors, and integrated robotics',
    chapters: 4,
    href: '/docs/module-4/chapter-13-walking-locomotion',
    color: 'orange',
  },
];

function ModuleCard({ title, icon, description, chapters, href, color }: ModuleItem) {
  const colorClass = `color-${color}`;
  return (
    <Link href={href} className={styles.cardLink}>
      <div className={clsx(styles.card, styles[colorClass])}>
        <div className={styles.iconContainer}>
          <span className={styles.icon}>{icon}</span>
        </div>
        <h3 className={styles.title}>{title}</h3>
        <p className={styles.description}>{description}</p>
        <div className={styles.footer}>
          <span className={styles.chapterCount}>{chapters} chapters</span>
          <span className={styles.arrow}>→</span>
        </div>
      </div>
    </Link>
  );
}

function QuickStartSection() {
  return (
    <section className={styles.quickStart}>
      <div className="container">
        <Heading as="h2" className={styles.sectionTitle}>
          🚀 Quick Start Guide
        </Heading>
        <div className={clsx('row', styles.stepsRow)}>
          <div className={clsx('col col--12 col--md--6 padding-vert--sm', styles.stepCol)}>
            <div className={styles.step}>
              <div className={styles.stepNumber}>1</div>
              <Heading as="h3">Choose Your Module</Heading>
              <p>Start with <strong>Module 1: Foundations</strong> if you're new to robotics, or jump to any module that interests you most.</p>
            </div>
          </div>
          <div className={clsx('col col--12 col--md--6 padding-vert--sm', styles.stepCol)}>
            <div className={styles.step}>
              <div className={styles.stepNumber}>2</div>
              <Heading as="h3">Follow the Curriculum</Heading>
              <p>Each chapter includes learning objectives, core concepts, code examples, hands-on exercises, and prerequisites.</p>
            </div>
          </div>
          <div className={clsx('col col--12 col--md--6 padding-vert--sm', styles.stepCol)}>
            <div className={styles.step}>
              <div className={styles.stepNumber}>3</div>
              <Heading as="h3">Use the AI Assistant</Heading>
              <p>Highlight text and ask questions for context-aware answers, or ask general questions about any topic in the textbook.</p>
            </div>
          </div>
          <div className={clsx('col col--12 col--md--6 padding-vert--sm', styles.stepCol)}>
            <div className={styles.step}>
              <div className={styles.stepNumber}>4</div>
              <Heading as="h3">Track Progress</Heading>
              <p>Monitor your learning journey with session history, explored topics, time spent, and learning milestones.</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function LearningOutcomes() {
  const outcomes = [
    'Write Python code for robotics simulations and control',
    'Design and analyze robotic systems using URDF models',
    'Implement computer vision and deep learning for robots',
    'Build reinforcement learning agents for robotics tasks',
    'Develop control algorithms for humanoid locomotion and manipulation',
    'Integrate multiple subsystems into complete robotic applications',
  ];

  return (
    <section className={styles.outcomes}>
      <div className="container">
        <Heading as="h2" className={styles.sectionTitle}>
          🎯 Learning Outcomes
        </Heading>
        <p className={styles.outcomesIntro}>
          By completing this Living Textbook, you will:
        </p>
        <div className={styles.outcomesList}>
          {outcomes.map((outcome, idx) => (
            <div key={idx} className={styles.outcomeItem}>
              <span className={styles.checkmark}>✓</span>
              <span>{outcome}</span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export default function Home(): JSX.Element {
  const { siteConfig } = useDocusaurusContext();

  return (
    <Layout title={siteConfig.title} description={siteConfig.tagline}>
      <HomepageHeader />
      <main>
        {/* Modules Section */}
        <section className={styles.modules}>
          <div className="container">
            <Heading as="h2" className={styles.sectionTitle}>
              📚 Choose Your Learning Path
            </Heading>
            <p className={styles.sectionSubtitle}>
              Explore our 4 carefully designed modules that take you from fundamental concepts to advanced humanoid robotics control:
            </p>
            <div className={clsx('row', styles.moduleRow)}>
              {ModulesList.map((props, idx) => (
                <div key={idx} className={clsx('col col--12 col--md--6 padding-vert--sm', styles.moduleCol)}>
                  <ModuleCard {...props} />
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Quick Start Section */}
        <QuickStartSection />

        {/* Learning Outcomes Section */}
        <LearningOutcomes />

        {/* CTA Section */}
        <section className={styles.cta}>
          <div className="container">
            <Heading as="h2">Ready to dive in?</Heading>
            <p>Start with your favorite module above, or begin with <Link to="/docs/module-1/chapter-1-python-intro">Chapter 1: Python Fundamentals</Link> if you're new to robotics.</p>
            <p className={styles.ctaSecondary}>Questions? Use the AI Teaching Assistant at the top of any chapter – it's ready to help!</p>
            <p className={styles.closing}>
              <strong>Happy Learning! 🚀</strong><br />
              <em>The future of robotics is in your hands. Let's build it together.</em>
            </p>
          </div>
        </section>
      </main>
    </Layout>
  );
}
