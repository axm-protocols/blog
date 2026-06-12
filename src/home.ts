// Home-page intro text (long-form, bilingual). Kept out of i18n.ts, which is for
// short UI labels. Each language is an array of paragraphs.
import type { Lang } from './i18n';

export const homeIntro: Record<Lang, { heading: string; tagline: string; paragraphs: string[] }> = {
  fr: {
    heading: 'L’IA et moi',
    tagline: 'Data scientist dans l’aéronautique. Je traite l’IA comme un collègue exigeant — notes sur l’autonomie, la rigueur, et le cadre qui rend les deux possibles.',
    paragraphs: [
      "Je suis data scientist dans l'aéronautique, passionné d'IA et de nouvelles technologies. J'utilise activement l'IA agentique depuis décembre 2025. En quelques mois, je n'en ai pas fait un simple assistant de plus : j'ai développé mon propre écosystème d'outils autour d'elle, pour qu'elle travaille comme je travaille. Je crée ce blog pour partager mes expériences et mes idées.",
      "Très vite, j'ai arrêté de voir l'IA comme un moteur de réponses. Je la traite comme un collègue à qui je délègue des tâches entières — mais un collègue sous contrat, avec des règles claires. D'abord l'autonomie : quand une tâche est claire, on l'exécute, sans me demander la permission à chaque étape ; on me dérange seulement pour une vraie décision. Ensuite l'opinion : quand je pose une question, j'attends une recommandation argumentée, pas cinq options équivalentes. Enfin la rigueur : je ne laisse rien partir tant que l'hypothèse n'a pas survécu à une tentative de la réfuter. Face à un bug, je ne devine pas la cause, je la mesure. Mesurer, falsifier, reformuler. Les idées vivent ou meurent par la donnée, pas par l'argument.",
      "Pour que tout ça tienne, j'ai construit un cadre. L'IA ne part pas dans le vide : elle suit des enchaînements de tâches avec des points de contrôle qui refusent de laisser passer un travail médiocre, elle inspecte la structure réelle du code au lieu de la deviner, et chaque test doit vraiment tester quelque chose. Le principe est simple : plus le cadre est clair, plus l'autonomie est sûre. La liberté sans structure produit du chaos ; la structure sans liberté produit de la lenteur. Je cherche les deux à la fois.",
      "Ce que je retiens, c'est que l'IA n'a pas remplacé mon jugement, elle l'a amplifié. Mal cadrée, elle amplifie la confusion ; bien cadrée, elle amplifie la rigueur. L'avenir n'appartient ni à ceux qui rejettent l'IA, ni à ceux qui lui délèguent aveuglément, mais à ceux qui savent en faire un collaborateur exigeant. C'est, au fond, exactement ce que j'attends d'un bon collègue humain.",
    ],
  },
  en: {
    heading: 'AI and me',
    tagline: 'Data scientist in aerospace. I treat AI as a demanding colleague — notes on autonomy, rigor, and the frame that makes both possible.',
    paragraphs: [
      "I'm a data scientist in aerospace, passionate about AI and new technology. I've been using agentic AI heavily since December 2025. In a few months I didn't just add one more assistant: I built my own ecosystem of tools around it, so it works the way I work. I'm starting this blog to share my experiments and ideas.",
      "I quickly stopped seeing AI as an answer engine. I treat it as a colleague I delegate whole tasks to — but a colleague under contract, with clear rules. First, autonomy: when a task is clear, it gets done, without asking permission at every step; I'm interrupted only for a real decision. Then, opinion: when I ask a question, I expect a reasoned recommendation, not five equivalent options. Finally, rigor: nothing ships until the hypothesis has survived an attempt to refute it. Facing a bug, I don't guess the cause, I measure it. Measure, falsify, reformulate. Ideas live or die by data, not by argument.",
      "To make all this hold, I built a frame. The AI doesn't wander: it follows task pipelines with checkpoints that refuse to let mediocre work through, it inspects the real structure of the code instead of guessing it, and every test must actually test something. The principle is simple: the clearer the frame, the safer the autonomy. Freedom without structure breeds chaos; structure without freedom breeds slowness. I want both at once.",
      "What I take away is that AI didn't replace my judgment — it amplified it. Poorly framed, it amplifies confusion; well framed, it amplifies rigor. The future belongs neither to those who reject AI, nor to those who delegate to it blindly, but to those who can make it a demanding collaborator. That is, in the end, exactly what I expect from a good human colleague.",
    ],
  },
};
