import {Config} from '@docusaurus/types';
import * as preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'Living Textbook with AI Teaching Assistant',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://giaic-hackathone.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/Physical-AI---Humanoid-Robotics-Book/',

  // GitHub pages deployment config
  organizationName: 'GIAIC-Hackathone',
  projectName: 'Physical-AI---Humanoid-Robotics-Book',
  trailingSlash: false,
  deploymentBranch: 'gh-pages',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internalization, you can use this field to set useful
  // metadata like html lang. For example, if your site is Chinese, you may want
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
          sidebarPath: require.resolve('./sidebars.js'),
          // Please change this to your repo.
          // Remove this line to remove the "edit this page" links.
          editUrl:
            'https://github.com/GIAIC-Hackathone/Physical-AI---Humanoid-Robotics-Book/tree/main/frontend',
        },
        blog: {
          showReadingTime: true,
          // Please change this to your repo.
          // Remove this line to remove the "edit this page" links.
          editUrl:
            'https://github.com/GIAIC-Hackathone/Physical-AI---Humanoid-Robotics-Book/tree/main/frontend',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      } as preset.Options,
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/docusaurus-social-card.jpg',
    navbar: {
      title: 'Living Textbook',
      logo: {
        alt: 'Physical AI Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Textbook',
        },
        {to: '/blog', label: 'Blog', position: 'left'},
        {
          href: 'https://github.com/GIAIC-Hackathone/Physical-AI---Humanoid-Robotics-Book',
          label: 'GitHub',
          position: 'right',
        },
      ],
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
              label: 'GitHub Issues',
              href: 'https://github.com/GIAIC-Hackathone/Physical-AI---Humanoid-Robotics-Book/issues',
            },
            {
              label: 'Discussions',
              href: 'https://github.com/GIAIC-Hackathone/Physical-AI---Humanoid-Robotics-Book/discussions',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'Blog',
              to: '/blog',
            },
            {
              label: 'GitHub',
              href: 'https://github.com/GIAIC-Hackathone/Physical-AI---Humanoid-Robotics-Book',
            },
          ],
        },
      ],
      copyright: `Copyright © 2025 GIAIC Hackathon. Built with Docusaurus.`,
    },
    prism: {
      theme: require('prism-react-renderer/themes/github'),
      darkTheme: require('prism-react-renderer/themes/dracula'),
    },
  } as any,
};

module.exports = config;
