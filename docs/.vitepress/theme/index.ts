import DefaultTheme from "vitepress/theme";
import "@catppuccin/vitepress/theme/mocha/sapphire.css";
import Theme from "vitepress/theme";
import './style.css'
import Layout from './layout.vue'

import "vitepress-markdown-timeline/dist/theme/index.css";

import vitepressNprogress from 'vitepress-plugin-nprogress';
import 'vitepress-plugin-nprogress/lib/css/index.css';

/* import SudokuSolver from './SudokuSolver.vue' */

import SudokuRunner from './SudokuRunner.vue'

import SudokuSolver from './SudokuSolver copy 2.vue'

export default {
  ...DefaultTheme,
  Layout: Layout,
  enhanceApp: (ctx) => {
    DefaultTheme.enhanceApp?.(ctx);
    vitepressNprogress(ctx);
    ctx.app.component('SudokuSolver', SudokuSolver)
    ctx.app.component('SudokuRunner', SudokuRunner)
  }
}