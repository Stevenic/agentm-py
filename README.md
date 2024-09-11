# AgentM

AgentM is a library of "Micro Agents" that make it easy to add reliable intelligence to any application. The philosophy behind AgentM is that "Agents" should be mostly comprised of deterministic code with a sprinkle of LLM-powered intelligence mixed in. Many of the existing Agent frameworks place the LLM at the center of the application as an orchestrator that calls a collection of tools. In an AgentM application, your code is the orchestrator, and you only call a micro agent when you need to perform a task that requires intelligence.

The initial draft of AgentM was written in JavaScript, but a Python version is available.

## Installation

To install and set up AgentM, simply run the `install.py` script. The script will prompt you to enter your OpenAI API key and the log directory:

```bash
python install.py
```

Sample output when running the installation script:

```bash
Enter your OpenAI API key: sk-xxxxxxx...
Enter the log directory path [default: ./var/logs/error.log]: 
Settings saved to config/settings.json
```

For more detailed information, please refer to the [INSTALL.md](INSTALL.md) file.

## Examples

### Example 1: Filter List

Run the **filter list** example to see how AgentM filters a list of items based on whether they are considered healthy snacks:

```bash
python examples/filter_list_example.py
```

#### Sample Output:
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

### Example 2: Sort List

Run the **sort list** example to see how AgentM sorts a list of items using LLM intelligence:

```bash
python examples/sort_list_example.py
```

#### Sample Output:
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
