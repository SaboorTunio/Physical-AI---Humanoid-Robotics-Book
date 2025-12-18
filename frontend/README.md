# Physical AI Living Textbook - Frontend

This is the **Docusaurus v3** powered frontend for the Living Textbook project. It serves the Physical AI & Humanoid Robotics curriculum as a static site deployed to GitHub Pages.

## Tech Stack

- **Docusaurus 3**: Static site generator with React components
- **React 18**: Interactive components (chat widget, highlighting)
- **TypeScript**: Type-safe development
- **Infima CSS**: Theming framework (included with Docusaurus)

## Project Structure

```
frontend/
├── docs/                 # Textbook content (16 chapters)
│   ├── intro.mdx
│   ├── module-1/        # Module 1: Foundations
│   ├── module-2/        # Module 2: The Body
│   ├── module-3/        # Module 3: The Brain
│   └── module-4/        # Module 4: Humanoid Control
├── src/
│   ├── components/      # React components (AiAssistant widget, etc)
│   ├── services/        # API service wrappers
│   ├── types/           # TypeScript types (generated from OpenAPI)
│   ├── styles/          # Custom CSS
│   └── utils/           # Helper functions
├── static/
│   └── img/             # Images, diagrams, logos
├── blog/                # Blog posts (optional)
├── docusaurus.config.ts # Main configuration
├── sidebars.ts          # Navigation structure
├── tsconfig.json        # TypeScript configuration
└── package.json         # Dependencies and scripts
```

## Getting Started

### Prerequisites

- Node.js 18+ (download from https://nodejs.org/)
- npm or yarn

### Installation

```bash
cd frontend
npm install
```

### Development Server

```bash
npm run start
```

This opens http://localhost:3000 in your browser with hot reload enabled.

### Build for Production

```bash
npm run build
```

Generates static site in `build/` directory.

### Serve Production Build

```bash
npm run serve
```

## Commands

| Command | Purpose |
|---------|---------|
| `npm run start` | Start development server (http://localhost:3000) |
| `npm run build` | Build static site to `/build` |
| `npm run serve` | Serve production build locally |
| `npm run clear` | Clear Docusaurus cache |
| `npm run deploy` | Deploy to GitHub Pages (requires GitHub Actions setup) |

## Adding Chapters

1. Create a new `.mdx` file in `docs/module-X/`:

```bash
touch docs/module-1/chapter-5-new-topic.mdx
```

2. Add YAML frontmatter with metadata:

```yaml
---
sidebar_position: 5
title: "Chapter 5: New Topic"
module: 1
part: 2
chapter_index: 5
learning_objectives:
  - Understand concept 1
  - Apply concept 2
prerequisites:
  - Chapter 4
keywords:
  - keyword1
  - keyword2
---
```

3. Write chapter content in Markdown/MDX (supports React components too)

4. The chapter automatically appears in the navigation sidebar

## Integrating the Chat Widget

The AI assistant chat widget is integrated globally on all pages. Located in:
- Component: `src/components/AiAssistant.tsx`
- Styles: `src/styles/assistant.css`

To customize the chat widget:

1. Edit `src/components/AiAssistant.tsx` (React component)
2. Update styles in `src/styles/assistant.css`
3. The widget automatically appears on every page

## Highlighting Text for Chat

Students can:
1. Highlight text in any chapter
2. A popup appears: "Ask AI about this"
3. Click to open chat with highlighted context
4. AI answers based on the highlighted text

Implementation:
- `src/components/ContextHighlight.tsx`: Capture text selection
- `src/services/api.ts`: Send highlighted text to backend

## Deployment

### GitHub Pages Deployment

The frontend automatically deploys to GitHub Pages when you push to `main`:

1. GitHub Actions workflow: `.github/workflows/frontend-deploy.yml`
2. Automatic deployment to: https://giaic-hackathone.github.io/Physical-AI---Humanoid-Robotics-Book/
3. Deployment status: Check GitHub Actions tab

### Manual Deployment

```bash
npm run deploy
```

## Troubleshooting

### Port 3000 Already in Use

```bash
# Find and kill process
lsof -ti:3000 | xargs kill -9

# Or use a different port
PORT=3001 npm run start
```

### Cache Issues

```bash
npm run clear
npm run start
```

### TypeScript Errors

```bash
npm run type-check
```

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make changes and test locally: `npm run start`
3. Build and verify: `npm run build`
4. Commit changes: `git commit -m "feat: description"`
5. Push to GitHub: `git push origin feature/your-feature`
6. Open a Pull Request

## Documentation

- [Docusaurus Docs](https://docusaurus.io/)
- [React Docs](https://react.dev/)
- [TypeScript Docs](https://www.typescriptlang.org/)

## Support

- GitHub Issues: Report bugs and feature requests
- Discussions: Ask questions and share ideas
- Documentation: See specs/ for detailed architecture

## License

Copyright © 2025 GIAIC Hackathon. Licensed under MIT.
