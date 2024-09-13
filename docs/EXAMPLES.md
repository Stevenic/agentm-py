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
```