import type {SidebarsConfig} from '@docusaurus/types';

const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    'intro',
    {
      label: 'Module 1: Foundations',
      collapsible: true,
      collapsed: false,
      items: [
        'module-1/chapter-1-python-intro',
        'module-1/chapter-2-simulation-basics',
        'module-1/chapter-3-math-robotics',
        'module-1/chapter-4-tools-setup',
      ],
    },
    {
      label: 'Module 2: The Body',
      collapsible: true,
      collapsed: false,
      items: [
        'module-2/chapter-5-sensors-overview',
        'module-2/chapter-6-actuators-control',
        'module-2/chapter-7-urdf-model',
        'module-2/chapter-8-kinematics',
      ],
    },
    {
      label: 'Module 3: The Brain',
      collapsible: true,
      collapsed: false,
      items: [
        'module-3/chapter-9-computer-vision',
        'module-3/chapter-10-pytorch-basics',
        'module-3/chapter-11-reinforcement-learning',
        'module-3/chapter-12-neural-networks',
      ],
    },
    {
      label: 'Module 4: Humanoid Control',
      collapsible: true,
      collapsed: false,
      items: [
        'module-4/chapter-13-walking-locomotion',
        'module-4/chapter-14-grasping-manipulation',
        'module-4/chapter-15-agentic-behaviors',
        'module-4/chapter-16-integration-project',
      ],
    },
  ],
};

export default sidebars;
