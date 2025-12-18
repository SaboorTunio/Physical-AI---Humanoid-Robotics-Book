import React from 'react';
import Link from '@docusaurus/Link';
import styles from './ModuleCard.module.css';

export interface ModuleCardProps {
  title: string;
  description: string;
  chapters: number;
  icon: string;
  href: string;
  color: string;
}

export const ModuleCard: React.FC<ModuleCardProps> = ({
  title,
  description,
  chapters,
  icon,
  href,
  color,
}) => {
  return (
    <Link href={href} className={styles.cardLink}>
      <div className={`${styles.card} ${styles[`color-${color}`]}`}>
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
};
