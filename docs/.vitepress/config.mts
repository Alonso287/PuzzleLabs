import { defineConfig } from 'vitepress';
/* import { SearchPlugin } from "vitepress-plugin-search"; */

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "PuzzleLabs",
  description: "Una guía sobre algoritmos de puzles",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Examples', link: '/markdown-examples' }
    ],

    sidebar: [
      {
        text: 'Examples',
        items: [
          { text: 'Markdown Examples', link: '/markdown-examples' },
          { text: 'Runtime API Examples', link: '/api-examples' }
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/Alonso287/PuzzleLabs' }
    ],

    search: {
      provider: 'local'
    }
  },

  markdown: {
    theme: {
      light: 'catppuccin-latte',
      dark: 'catppuccin-mocha',
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
/*   vite: { plugins: [SearchPlugin(options)]} */
})
