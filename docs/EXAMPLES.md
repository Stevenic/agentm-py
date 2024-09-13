# AgentM Examples

This document contains detailed examples of how to use the micro-agents in AgentM. Here, we walk through practical use cases and outputs to help you understand how the library functions in various scenarios.

For more general information and a quick overview, refer to the [README](../README.md).

## Example 1: Filter List

Run the **filter list** example to see how AgentM filters a list of items based on whether they are considered healthy snacks:

```bash
python examples/filter_list_example.py
```

### Sample Output:
```bash
Original list: ['Apple', 'Chocolate bar', 'Carrot', 'Chips', 'Orange']

Filtered results:

{'explanation': 'The apple is a healthy snack option, as it is low in calories, rich in fiber, and provides essential vitamins such as vitamin C.', 'remove_item': False}
{'explanation': 'A chocolate bar is generally considered an unhealthy snack because it is high in sugar and saturated fats, which can contribute to weight gain and other health issues if consumed in excess.', 'remove_item': True}
{'explanation': 'Carrots are a healthy snack option, as they are low in calories, high in fiber, and rich in vitamins and minerals.', 'remove_item': False}
{'explanation': 'Chips are typically high in unhealthy fats, sodium, and calories, making them a less nutritious snack choice...', 'remove_item': True}
{'explanation': 'The orange is a healthy snack option, as it is low in calories and high in vitamin C and dietary fiber, making it a nutritious choice.', 'remove_item': False}

Final Filtered List: ['Apple', 'Carrot', 'Orange']
```

## Example 2: Sort List

Run the **sort list** example to see how AgentM sorts a list of items using LLM intelligence:

```bash
python examples/sort_list_example.py
```

### Sample Output:
```bash
2024-09-11 10:46:22,401 - INFO - Sending batch comparison request with prompt: Compare Apple and Orange and return the items in the correct order as 'item1,item2'.
2024-09-11 10:46:22,729 - INFO - Received response: Apple,Orange
2024-09-11 10:46:22,730 - INFO - Sending batch comparison request with prompt: Compare Grape and Pineapple and return the items in the correct order as 'item1,item2'.
2024-09-11 10:46:23,094 - INFO - Received response: Grape,Pineapple
2024-09-11 10:46:23,094 - INFO - Sending batch comparison request with prompt: Compare Banana and Grape and return the items in the correct order as 'item1,item2'.
2024-09-11 10:46:23,539 - INFO - Received response: Banana,Grape
2024-09-11 10:46:23,540 - INFO - Sending batch comparison request with prompt: Compare Apple and Banana and return the items in the correct order as 'item1,item2'.
Compare Orange and Grape and return the items in the correct order as 'item1,item2'.
2024-09-11 10:46:24,067 - INFO - Received response: Apple,Banana  
Grape,Orange
Original list: ['Apple', 'Orange', 'Banana', 'Grape', 'Pineapple']
Sorted list: ['Apple', 'Banana', 'Orange', 'Grape', 'Pineapple']
```

## Example 3: Chain of Thought

Run the **chain of thought** example to see how AgentM solves problems using a step-by-step reasoning approach:

```bash
python examples/chain_of_thought_example.py
```

### Sample Output:
```bash
Question: What is the square root of 144?
Chain of Thought Reasoning: To find the square root of 144 step-by-step, follow these steps:

1. **Understanding Square Roots**: The square root of a number is a value that, when multiplied by itself, gives that number. For example, if x is the square root of y, then x * x = y.

2. **Identifying the Number**: In this case, we need to find the square root of 144.

3. **Finding Factors**: We'll look for a number that, when multiplied by itself, equals 144. 

4. **Testing Numbers**: 
   - Let's start with smaller numbers:
     - 1 * 1 = 1 (not the answer)
     - 2 * 2 = 4 (not the answer)
     - 3 * 3 = 9 (not the answer)
     - 4 * 4 = 16 (not the answer)
     - 5 * 5 = 25 (not the answer)
     - 6 * 6 = 36 (not the answer)
     - 7 * 7 = 49 (not the answer)
     - 8 * 8 = 64 (not the answer)
     - 9 * 9 = 81 (not the answer)
     - 10 * 10 = 100 (not the answer)
     - 11 * 11 = 121 (not the answer)
     - 12 * 12 = 144 (this is the answer)
   
5. **Conclusion**: The square root of 144 is 12.

Thus, the final answer is:

\[
\sqrt{144} = 12
\]
```

## Example 4: Binary Classification List

Run the **binary classification list** example to classify items as healthy or unhealthy:

```bash
python examples/binary_classify_list_example.py
```

### Sample Output:
```bash
Classifying item: Based on the following criteria 'Classify each item as either healthy (true) or unhealthy (false)', classify the item 'Apple' as true or false.
Received response for item: Based on the following criteria 'Classify each item as either healthy (true) or unhealthy (false)', classify the item 'Apple' as true or false. -> True
Classifying item: Based on the following criteria 'Classify each item as either healthy (true) or unhealthy (false)', classify the item 'Chocolate' as true or false.
Received response for item: Based on the following criteria 'Classify each item as either healthy (true) or unhealthy (false)', classify the item 'Chocolate' as true or false. -> Chocolate can be classified as unhealthy (false) if it contains high levels of sugar and fat, such as most commercially available milk chocolates. However, dark chocolate with a high cocoa content (70% or more) has health benefits and can be considered healthy in moderation. 

Without specific context, the classification can vary. Generally:

- If we consider typical chocolate, it would be classified as unhealthy (false).
- If it is high-quality dark chocolate and consumed in moderation, it could be classified as healthy (true).

For general classification, I would classify 'Chocolate' as unhealthy (false).
Classifying item: Based on the following criteria 'Classify each item as either healthy (true) or unhealthy (false)', classify the item 'Carrot' as true or false.
Received response for item: Based on the following criteria 'Classify each item as either healthy (true) or unhealthy (false)', classify the item 'Carrot' as true or false. -> True
Original list: ['Apple', 'Chocolate', 'Carrot']
Binary classified results: [{'item': "Based on the following criteria 'Classify each item as either healthy (true) or unhealthy (false)', classify the item 'Apple' as true or false.", 'classification': 'True'}, {'item': "Based on the following criteria 'Classify each item as either healthy (true) or unhealthy (false)', classify the item 'Chocolate' as true or false.", 'classification': "Chocolate can be classified as unhealthy (false) if it contains high levels of sugar and fat, such as most commercially available milk chocolates. However, dark chocolate with a high cocoa content (70% or more) has health benefits and can be considered healthy in moderation. \n\nWithout specific context, the classification can vary. Generally:\n\n- If we consider typical chocolate, it would be classified as unhealthy (false).\n- If it is high-quality dark chocolate and consumed in moderation, it could be classified as healthy (true).\n\nFor general classification, I would classify 'Chocolate' as unhealthy (false)."}, {'item': "Based on the following criteria 'Classify each item as either healthy (true) or unhealthy (false)', classify the item 'Carrot' as true or false.", 'classification': 'True'}]
```# AgentM Examples (Continued)

## Example 5: Project List

Run the **project list** example to project items based on a rule:

```bash
python examples/project_list_example.py
```

### Sample Output:

```bash
Original list: ['Apple', 'Banana', 'Carrot']
Projected results: [{'item': "Project the following item based on the rule 'Project these items as their vitamin content': Apple.", 'projection': "Apples are known for their vitamin content, particularly vitamin C. A medium-sized apple typically contains about 14% of the daily value of vitamin C. Additionally, apples provide small amounts of other vitamins such as vitamin A and some B vitamins (like B6 and riboflavin), but their overall vitamin content is modest compared to other fruits. \n\nTherefore, based on the rule 'Project these items as their vitamin content,' the projected vitamin content for an apple would primarily highlight its contribution of vitamin C."}, {'item': "Project the following item based on the rule 'Project these items as their vitamin content': Banana.", 'projection': "Bananas are known for their nutrient content, particularly their vitamins. Here's a projection of the vitamin content found in a banana:\n\n- **Vitamin B6**: Bananas are an excellent source of Vitamin B6, which plays a crucial role in metabolism and brain health.\n- **Vitamin C**: They contain a moderate amount of Vitamin C, which is important for immune function and skin health.\n- **Vitamin A**: Present in smaller amounts, Vitamin A supports vision and immune health.\n- **Folate (Vitamin B9)**: Bananas provide some folate, which is essential for cell division and DNA synthesis.\n\nIn summary, bananas are primarily valued for their high Vitamin B6 content, along with contributions of Vitamin C, Vitamin A, and Folate."}, {'item': "Project the following item based on the rule 'Project these items as their vitamin content': Carrot.", 'projection': 'Carrots are known for their high vitamin content, particularly vitamin A. Here’s the projected vitamin content based on that focus:\n\n- **Vitamin A**: Carrots are rich in beta-carotene, which the body converts into vitamin A. This vitamin is important for vision, immune function, and skin health.\n- **Vitamin K1**: Essential for blood clotting and bone health.\n- **Vitamin B6**: Important for metabolism and brain health.\n- **Vitamin C**: Contributes to immune function and skin health.\n\nOverall, carrots can be projected as a nutrient-dense food with a strong emphasis on vitamin A and a good mix of other vitamins.'}]
```

## Example 6: Generate Object

Run the **generate object** example to create an object based on a description:

```bash
python examples/generate_object_example.py
```

### Sample Output:

```bash
Object description: A machine that can sort fruits.
Generated object: {'object_description': 'A machine that can sort fruits.', 'generated_object': '**High-Level Design of a Fruit Sorting Machine**\n\n**Machine Overview:**\nThe Fruit Sorting Machine is an automated system designed to efficiently categorize and sort various types of fruit based on size, color, weight, and quality. The machine aims to streamline the sorting process, reduce manual labor, and enhance consistency in fruit processing.\n\n**Components:**\n\n1. **Fruit Input Hopper:**\n   - Description: A large funnel-shaped container where fruits are initially loaded.\n   - Features: Adjustable height, vibration mechanism to prevent jamming, and a safety cover.\n\n2. **Conveyor Belt System:**\n   - Description: A series of conveyor belts that transport fruits from the input hopper to the sorting area.\n   - Features: Adjustable speed settings, rubberized surface for grip, and incline/decline options for gravity-assisted sorting.\n\n3. **Image Recognition System:**\n   - Description: A series of high-resolution cameras positioned above the conveyor belt.\n   - Function: Capture real-time images of the fruits as they pass by for size, color, and quality analysis using advanced image processing software.\n\n4. **Weight Measurement Station:**\n   - Description: A designated area on the conveyor belt equipped with load cells.\n   - Function: Measure the weight of each fruit to sort them according to predefined weight categories.\n\n5. **Sorting Mechanism:**\n   - Description: A combination of pneumatic actuators and mechanical arms.\n   - Function: Based on data from image recognition and weight measurement, fruits are directed to specific sorting paths.\n   - Features: Quick-release mechanisms for rapid sorting and adjustable sorting paths for various fruit types.\n\n6. **Output Bins:**\n   - Description: Several storage bins placed at the end of the sorting path to collect sorted fruits.\n   - Function: Each bin is designated for a specific category based on size, weight, and quality.\n   - Features: Labeling system for easy identification and removable for cleaning and maintenance.\n\n7. **Control Panel:**\n   - Description: A user-friendly interface for operators to set sorting parameters, monitor performance, and troubleshoot.\n   - Features: Touchscreen display, emergency stop button, and connectivity for remote monitoring.\n\n8. **Power Supply System:**\n   - Description: A robust electrical system to power all components of the machine.\n   - Features: Energy-efficient motors and backup battery support to ensure continuous operation.\n\n9. **Support Frame:**\n   - Description: The structural framework supporting all components.\n   - Features: Adjustable height settings, made of durable materials (stainless steel/aluminum) to resist wear and corrosion.\n\n**Workflow Summary:**\n1. Fruits are loaded into the input hopper.\n2. The conveyor belt transports the fruits to the image recognition system, where they are scanned for size and color.\n3. Fruits then pass over the weight measurement station to determine their weight.\n4. The sorting mechanism utilizes data from the recognition and weighing systems to direct each fruit into the appropriate output bin.\n5. Sorted fruits collected in designated bins can then be packaged or processed further.\n\n**Additional Considerations:**\n- Potential integration with a data management system to log sorting data for future analysis.\n- Implementation of a cleaning system to ensure hygiene, especially for perishable fruits.\n- Safety features to protect operators, such as shielded moving parts and emergency stops.\n\nThis high-level design outlines the fundamental components and workflow of a fruit sorting machine that works efficiently, accurately, and safely, fulfilling the needs of agricultural and food processing industries.'}
```

## Example 7: Map List

Run the **map list** example to apply transformations to list items:

```bash
python examples/map_list_example.py
```

### Sample Output:

```bash
Original list: ['Apple', 'Banana', 'Carrot']
Transformed list: ['APPLE', 'BANANA', 'CARROT']
```

## Example 8: Reduce List

Run the **reduce list** example to reduce items to achieve a specific goal:

```bash
python examples/reduce_list_example.py
```

### Sample Output:

```bash
Original list: ['Banana', 'Apple', 'Carrot']
Reduced results: [{'item': "Reduce the item 'Banana' to achieve the goal: Reduce these items to a single word representing their nutritional value.", 'reduced_item': 'Fruit'}, {'item': "Reduce the item 'Apple' to achieve the goal: Reduce these items to a single word representing their nutritional value.", 'reduced_item': 'Fruit'}, {'item': "Reduce the item 'Carrot' to achieve the goal: Reduce these items to a single word representing their nutritional value.", 'reduced_item': 'Beta-carotene'}]
```

## Example 9: Summarize List

Run the **summarize list** example to generate concise summaries:

```bash
python examples/summarize_list_example.py
```

### Sample Output:

```bash
Original list: ['The quick brown fox jumps over the lazy dog.', 'Python is a popular programming language.']
Summarized results: [{'item': 'Summarize the following: The quick brown fox jumps over the lazy dog..', 'summary': 'A swift brown fox leaps over a sluggish dog.'}, {'item': 'Summarize the following: Python is a popular programming language..', 'summary': 'Python is a widely used programming language known for its simplicity and versatility.'}]
```