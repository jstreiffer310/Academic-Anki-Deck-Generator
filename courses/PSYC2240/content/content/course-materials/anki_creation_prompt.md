# Anki Deck Creation Prompt for PSYC 2240 - Biological Basis of Behaviour

## Task Overview
Create a comprehensive Anki flashcard deck in CSV format for studying chapters 1-3 of a biological psychology course. The deck should focus on terms, definitions, and key concepts that appear in BOTH the textbook notes and lecture materials.

## Source Materials Available
1. **Textbook Notes (.docx file)** - Contains highlighted terms and definitions (green highlighting indicates key terms)
2. **Lecture 1 Slides (PDF)** - September 3, 2022 lecture content
3. **Lecture 2 Slides (PDF)** - September 10 lecture content  
4. **Lecture Transcripts** - Actual spoken content from lectures
5. **Pop Quiz content** - Additional discussion material

## Key Requirements

### Content Focus
- **Primary Focus**: Terms and concepts that appear in BOTH textbook notes AND lecture slides/transcripts
- **Chapters**: Specifically chapters 1, 2, and 3 content
- **Green Highlighted Terms**: Pay special attention to terms highlighted in green in the textbook notes - these are key definitions
- **Images**: Use OCR to extract text from any relevant images in the materials, as there may be important diagrams or concept maps

### Card Types to Create
1. **Term → Definition cards**
   - Front: Key term
   - Back: Complete definition

2. **Concept → Explanation cards**
   - Front: Important concept or phenomenon
   - Back: Detailed explanation with examples

3. **Function → Structure cards**
   - Front: "What brain structure is responsible for..."
   - Back: Specific brain region/structure

4. **Example → Category cards**
   - Front: Specific example or case study
   - Back: General principle or category it represents

### CSV Format Requirements
```
Front,Back,Tags
"What is a neuron?","Specialised nervous system cells engaged in information processing","Chapter1,BasicTerms,Neurons"
```

### Content Areas to Cover
Based on the materials, focus on:

1. **Chapter 1 Topics:**
   - Brain and behavior fundamentals
   - TBI and concussion
   - Why study brain + behavior
   - Brain structure basics (CNS, PNS, cerebrum, etc.)
   - Clinical conditions (locked-in syndrome, minimally conscious state)

2. **Chapter 2 Topics:**
   - Neuron anatomy and function
   - Glial cells
   - Brain anatomy (hemispheres, neocortex, brainstem, cerebellum)
   - Action potentials and neural communication
   - Reflexes and neural networks

3. **Chapter 3 Topics:**
   - Genetics and behavior
   - Evolutionary principles
   - Genetic disorders affecting the brain
   - Inheritance patterns

### Quality Guidelines
- **Accuracy**: Ensure all definitions match both textbook and lecture content
- **Completeness**: Include specific examples mentioned in lectures
- **Clarity**: Write definitions in clear, concise language
- **Cross-referencing**: When the same concept appears in multiple sources, synthesize the information
- **Tags**: Use consistent tagging system (Chapter1, Chapter2, Chapter3, BasicTerms, ClinicalCases, etc.)

### Special Instructions
1. **Image Processing**: If images contain text, diagrams, or concept maps, use OCR to extract and include relevant textual information
2. **Lecture Integration**: Include specific examples, analogies, or explanations that the professor provided in lectures
3. **Clinical Focus**: Pay attention to clinical examples and case studies (like Martin Pistorius, hemispatial neglect, etc.)
4. **Prioritization**: Focus on concepts that appear in multiple sources as these are likely exam-relevant

### Output Format
- Provide a CSV file ready for direct import into Anki
- Include a separate file with a summary of:
  - Total number of cards created
  - Breakdown by chapter and card type
  - List of key terms that appear in both textbook and lectures
  - Any important concepts found in images via OCR

### Example Cards Based on Available Content
```
"What is hemispatial neglect?","A condition where patients neglect one side of space due to brain damage, typically affecting the left side after right hemisphere damage","Chapter1,ClinicalCases,SpatialProcessing"

"What is the vestibular ocular reflex (VOR)?","A three-neuron reflex that allows you to keep your eyes fixed on an object while moving your head","Chapter2,Reflexes,MotorControl"

"What are the main components of the central nervous system?","The brain and spinal cord, which together mediate behaviour and are encased in bone","Chapter1,BasicTerms,Anatomy"
```

Create comprehensive flashcards that will help a student master the foundational concepts in biological psychology, emphasizing the integration between textbook knowledge and lecture content.