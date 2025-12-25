import {Config} from '@docusaurus/types';
import * as preset from '@docusaurus/preset-classic';
import path from 'path';
import {fileURLToPath} from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const config: Config = {
  title: 'Physical AI & Humanoid Robotics Textbook',
  tagline: 'Interactive Learning with AI Teaching Assistant',
  favicon: '/img/favicon.svg',

  // Set the production url of your site here
  url: 'https://giaic-hackathone.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  // GitHub pages deployment config
  organizationName: 'GIAIC-Hackathone',
  projectName: 'Physical-AI---Humanoid-Robotics-Book',
  trailingSlash: false,
  deploymentBranch: 'gh-pages',

  onBrokenLinks: 'warn',
  markdown: {
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
  },

  // Even if you don't use internalization, you can use this field to set useful
  // metadata like html lang. For example, if your user is Chinese, you may want
  // to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: path.resolve(__dirname, './sidebars.ts'),
          // Please change this to your repo.
          // Remove this line to remove the "edit this page" links.
          editUrl:
            'https://github.com/panaversity',
        },
        blog: {
          showReadingTime: true,
          // Please change this to your repo.
          // Remove this line to remove the "edit this page" links.
          editUrl:
            'https://github.com/GIAIC-Hackathone/Physical-AI---Humanoid-Robotics-Book/tree/main/frontend',
        },
        theme: {
          customCss: path.resolve(__dirname, './src/css/custom.css'),
        },
      } as preset.Options,
    ],
  ],

  themes: ['@docusaurus/theme-live-codeblock'],
  themeConfig: {
    metadata: [
      {name: 'keywords', content: 'robotics, AI, textbook, education, humanoid robotics'},
      {name: 'theme-color', content: '#2563eb'},
    ],
    navbar: {
      title: 'Physical AI & Humanoid Robotics Textbook',
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Textbook',
        },
        {
          href: 'https://github.com/SaboorTunio',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    // Add the Root component to wrap the entire app
    announcementBar: {
      id: 'teaching_assistant',
      content: '🤖 AI Teaching Assistant is now available! Click the robot icon to ask questions about the content.',
      backgroundColor: '#6e8efb',
      textColor: '#fff',
      isCloseable: true,
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'Textbook',
              to: '/docs/intro',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'GitHub Panaversity',
              href: 'https://github.com/Panaversity',
            },
           
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/SaboorTunio',
            },
          ],
        },
      ],
      copyright: `Copyright © 2025 Abdul Saboor Tunio | Built with passion & code.`,
    },
    prism: {
      additionalLanguages: ['python', 'javascript', 'typescript', 'bash', 'json'],
    },
  } as any,
};

export default config;
