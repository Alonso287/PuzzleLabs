import DefaultTheme from "vitepress/theme";
import "@catppuccin/vitepress/theme/mocha/sapphire.css";
import Theme from "vitepress/theme";

import "vitepress-markdown-timeline/dist/theme/index.css";

import vitepressNprogress from 'vitepress-plugin-nprogress';
import 'vitepress-plugin-nprogress/lib/css/index.css';

export default {
  ...DefaultTheme,
  enhanceApp: (ctx) => {
    vitepressNprogress(ctx);
  }
}