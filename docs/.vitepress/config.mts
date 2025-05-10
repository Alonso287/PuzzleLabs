import { defineConfig } from 'vitepress';
import timeline from "vitepress-markdown-timeline";

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "PuzzleLabs",
  description: "Una guía sobre algoritmos de puzles",
  lastUpdated: true,  

  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config


    nav: [
      { text: 'Inicio', link: '/' },
      { text: 'Acerca de ', link: 'about'},
      { text: 'Changelog', link: 'https://github.com/Alonso287/PuzzleLabs/commits/main/'},
      { text: 'Local', link: 'http://localhost:5173', target: '_self' },
      { text: 'Vercel', link: 'https://puzzlelabs.vercel.app/', target:'_self'}
    ],

    sidebar: [
      {
        text: 'Introducción',
        link: 'intro',
      },
      {
        text: 'Acerca de',
        link: 'about',
      },
      {
        text: 'Roadmap',
        link: 'roadmap',
      },
      {
        text: 'Sudoku',
        collapsed: false,
        items: [
          {text: 'Introducción', link: '/sudoku/intro'},
          {text: 'Algoritmo de creación', link: '/sudoku/maker'},
          {text: 'Algoritmo de resolución', link: '/sudoku/solver'},
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/Alonso287/PuzzleLabs' }
    ],

    search: {
      provider: 'local'
    },
    
    logo: '/favicon/favicon.svg',
    siteTitle: false,

    footer: {
      message: 'PuzzleLabs',
      copyright: 'Copyright © 2025 Alonso Navarro'
    },

    editLink:{
      pattern: 'https://github.com/Alonso287/PuzzleLabs/edit/main/docs/:path',
      text: 'Editar esta página en GitHub',
    },

    lastUpdated: {
      text: 'Última actualización',
      formatOptions: {
        dateStyle: 'full',
        timeStyle: 'medium'
      }
    }
  },

  markdown: {
    theme: {
      light: 'catppuccin-latte',
      dark: 'catppuccin-mocha',
    },
    config: (md) => {
      md.use(timeline);
    },
  },

  head: [
    [
      'link', 
      { rel: 'icon', 
        type:"image/png", 
        href: '/favicon/favicon-96x96.png',
        sizes:'96x96' 
      }
    ],
    [
      'link', 
      { rel: 'icon', 
        type:"image/svg+xml", 
        href: '/favicon/favicon.svg'
      }
    ],
    [
      'link', 
      { rel: 'shortcut icon', 
        href: '/favicon/favicon.ico' 
      }
    ],    
    [
      'link', 
      { rel: 'apple-touch-icon', 
        href: '/favicon/apple-touch-icon.png',
        sizes:'180x180' 
      }
    ],
    [
      'meta', 
      { name: 'apple-mobile-web-app-title', 
        content: 'PuzzleLabs'
      }
    ],
    [
      'link', 
      { rel: 'manifest', 
        href: '/favicon/site.webmanifest'
      }
    ],
  ],
});