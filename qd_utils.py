def get_prompt(test_user, few_shot_examples, sys_prompt):
    prompt_messages = [
        {
            "role": "system",
            "content": sys_prompt
        }
    ]

    for example in few_shot_examples:
        ex_user = example[0]
        ex_assistant = example[1]
        prompt_messages.extend([
            {
                "role": "user",
                "content": ex_user
            },
            {
                "role": "assistant",
                "content": ex_assistant
            }
        ])

    prompt_messages.append(
        {
            "role": "user",
            "content": test_user
        }
    )

    return prompt_messages


def pretty_print_prompt(prompt, log_file_ptr=None):
    for message_item in prompt:
        print(f"{message_item['role'].upper()}\n", file=log_file_ptr)
        print(f"{message_item['content']}\n\n", file=log_file_ptr)
