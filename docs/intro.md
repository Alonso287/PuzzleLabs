---
prev: false
next: false
---
<script setup>
import { VPTeamMembers } from 'vitepress/theme'

const members = [
  {
    avatar: '/alonso.jpg',
    name: 'Alonso',
    title: 'Creador',
    links: [
      { icon: 'github', link: 'https://github.com/Alonso287' },
      { icon: 'instagram', link: 'https://instagram.com/alonsonavarroserrano' }
    ]
  },
]
</script>

# Introducción

¡Bienvenido a PuzzleLabs! He creado esta página para aprender a crear algoritmos que creen y resuelvan distintos tipos de puzles.
En esta página encontrarás diferentes guías en las que analizaremos el juego en profundidad, investigaremos sobre las normas y patrones comunes para luego crear programas que puedan crear y resolver estos problemas, a través de la lógica, las matemáticas y la programación.
Ten en cuenta que las guías no irán directamente a la solución, sino que iremos averiguando poco a poco la solución, una mezcla entre blog y guía con un propósito más didáctico.

Tengo planeado programar los algoritmos que vayamos creando en Python, pero por desgracia todavía no he aprendido a programar, así que tendré que esperar a un futuro para hacerlo.

Todo el proyecto es de código abierto y puedes ver el código fuente en [mi repositorio de GitHub](https://github.com/Alonso287/PuzzleLabs), y también puedes ver un [roadmap](roadmap) con los distintos objetivos y puzles que se irán añadiendo en un futuro.

El **código** mostrado en esta página está bajo licencia [AGPL v3.0](https://www.gnu.org/licenses/agpl-3.0.html), y el **contenido educativo** (textos, explicaciones, diagramas) está bajo licencia [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

<div style="display: flex; justify-content: center;">
  <VPTeamMembers size="medium" :members="members" />
</div>