import { defineConfig } from 'vitepress';
import timeline from "vitepress-markdown-timeline";
import { withMermaid } from 'vitepress-plugin-mermaid';

export default withMermaid(

// https://vitepress.dev/reference/site-config

  defineConfig({
    title: "PuzzleLabs",
    description: "Una guía sobre algoritmos de puzles",
    lastUpdated: true,  
    cleanUrls: true,
    lang: 'es-ES',

    mermaid: {
      theme: "neutral",
    },

    themeConfig: {

      // https://vitepress.dev/reference/default-theme-config

      nav: [
        { text: 'Inicio', link: '/' },
        { text: 'Acerca de ', link: 'about'},
        { text: '0.8',
          items: [
            { text: 'Roadmap', link: 'roadmap'},
            { text: 'Changelog', link: 'https://github.com/Alonso287/PuzzleLabs/commits/main/'},
            { text: 'Local', link: 'http://localhost:5173', target: '_self' },
            { text: 'Vercel', link: 'https://puzzlelabs.vercel.app/', target:'_self'}
          ]
        },
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
            {text: 'Resolución',
            collapsed: true,
              items: [
                {text: 'Métodos de resolución', link: '/sudoku/solver/solving'},
                {text: 'Algoritmo de resolución', link: '/sudoku/solver/solving-alg'},
            ]
            },
            {text: 'Creación', link: '/sudoku/making'},
          ]
        }
      ],

      socialLinks: [
        { icon: 'github', link: 'https://github.com/Alonso287/PuzzleLabs' }
      ],

      search: {
        provider: 'local',
        options: {
          locales: {
            root: {
              translations: {
                button: {
                  buttonText: 'Buscar',
                  buttonAriaLabel: 'Buscar'
                },
                modal: {
                  displayDetails: 'Mostrar detalles',
                  resetButtonTitle: 'Borrar',
                  backButtonTitle: 'Volver',
                  noResultsText: 'No se encontraron resultados para',
                  footer: {
                    selectText: 'para seleccionar',
                    selectKeyAriaLabel: 'para seleccionar',
                    navigateText: 'para navegar',
                    navigateUpKeyAriaLabel: 'flecha arriba',
                    navigateDownKeyAriaLabel: 'flecha abajo',
                    closeText: 'para cerrar',
                    closeKeyAriaLabel: 'esc'
                  }
                }
              }
            },
          }
        }
      },

      logo: {
        light: '/favicon/claro.svg',
        dark: '/favicon/oscuro.svg',
      },
      
      siteTitle: false,

      footer: {
        message: 'Contenido bajo  <a href="https://creativecommons.org/licenses/by-sa/4.0/" target="_blank" rel="noopener noreferrer">CC BY-SA 4.0</a> · Código bajo <a href="https://www.gnu.org/licenses/agpl-3.0.html" target="_blank" rel="noopener noreferrer">AGPL-3.0</a>',
        copyright: 'PuzzleLabs · © 2025 Alonso Navarro'
      },

      editLink:{
        pattern: 'https://github.com/Alonso287/PuzzleLabs/edit/main/docs/:path',
        text: 'Editar esta página en GitHub',
      },

      lastUpdated: {
        text: 'Última actualización',
        formatOptions: {
          dateStyle: 'short',
          timeStyle: 'short'
        }
      },

      docFooter: {
        prev: 'Página anterior',
        next: 'Página siguiente'
      },

      darkModeSwitchLabel: 'Apariencia',
      lightModeSwitchTitle: 'Cambiar al modo claro',
      darkModeSwitchTitle: 'Cambiar al modo oscuro',
      sidebarMenuLabel: 'Menú',
      returnToTopLabel: 'Volver arriba',
      langMenuLabel: 'Seleccionar idioma',
      skipToContentLabel: 'Saltar al contenido',
      outlineTitle: 'En esta página',
    },

    markdown: {
      math: true,
      container: {
        tipLabel: 'Consejo',
        warningLabel: 'Atención',
        dangerLabel: 'Peligro',
        infoLabel: 'Información',
        detailsLabel: 'Detalles'
      },
      image: {
        // image lazy loading is disabled by default
        lazyLoading: false
      },
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
  })
)