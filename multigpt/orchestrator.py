from autogpt.config import Config
from multigpt.expert import Expert
from multigpt.multi_prompt_generator import MultiPromptGenerator


class Orchestrator(Expert):
    # TODO make get_prompt from prompt.py a method of expert and ochestrator
    def get_prompt(self):
        """
        This function generates a prompt string that includes various constraints,
            commands, resources, and performance evaluations.

        Returns:
            str: The generated prompt string.
        """

        # Initialize the Config object
        cfg = Config()

        # Initialize the PromptGenerator object
        prompt_generator = MultiPromptGenerator()

        # Add constraints to the PromptGenerator object
        prompt_generator.add_constraint(
            "~4000 word limit for short term memory. Your short term memory is short, so"
            " immediately save important information to files."
        )
        prompt_generator.add_constraint(
            "If you are unsure how you previously did something or want to recall past"
            " events, thinking about similar events will help you remember."
        )
        prompt_generator.add_constraint("No user assistance")
        prompt_generator.add_constraint(
            'Exclusively use the commands listed in double quotes e.g. "command name"'
        )

        # Define the command list
        commands = [
            ("Google Search", "google", {"input": "<search>"}),
            (
                "Browse Website",
                "browse_website",
                {"url": "<url>", "question": "<what_you_want_to_find_on_website>"},
            ),
            (
                "Start GPT Agent",
                "start_agent",
                {"name": "<name>", "task": "<short_task_desc>", "prompt": "<prompt>"},
            ),
            (
                "Message GPT Agent",
                "message_agent",
                {"key": "<key>", "message": "<message>"},
            ),
            ("List GPT Agents", "list_agents", {}),
            ("Delete GPT Agent", "delete_agent", {"key": "<key>"}),
            (
                "Clone Repository",
                "clone_repository",
                {"repository_url": "<url>", "clone_path": "<directory>"},
            ),
            ("Write to file", "write_to_file", {"file": "<file>", "text": "<text>"}),
            ("Read file", "read_file", {"file": "<file>"}),
            ("Append to file", "append_to_file", {"file": "<file>", "text": "<text>"}),
            ("Delete file", "delete_file", {"file": "<file>"}),
            ("Search Files", "search_files", {"directory": "<directory>"}),
            ("Evaluate Code", "evaluate_code", {"code": "<full_code_string>"}),
            (
                "Get Improved Code",
                "improve_code",
                {"suggestions": "<list_of_suggestions>", "code": "<full_code_string>"},
            ),
            (
                "Write Tests",
                "write_tests",
                {"code": "<full_code_string>", "focus": "<list_of_focus_areas>"},
            ),
            ("Execute Python File", "execute_python_file", {"file": "<file>"}),
            ("Generate Image", "generate_image", {"prompt": "<prompt>"}),
            ("Send Tweet", "send_tweet", {"text": "<text>"}),
        ]

        # Only add the audio to text command if the model is specified
        if cfg.huggingface_audio_to_text_model:
            commands.append(
                (
                    "Convert Audio to text",
                    "read_audio_from_file",
                    {"file": "<file>"}
                ),
            )

        # Only add shell command to the prompt if the AI is allowed to execute it
        if cfg.execute_local_commands:
            commands.append(
                (
                    "Execute Shell Command, non-interactive commands only",
                    "execute_shell",
                    {"command_line": "<command_line>"},
                ),
            )

        # Add these command last.
        commands.append(
            ("Do Nothing", "do_nothing", {}),
        )
        commands.append(
            ("Task Complete (Shutdown)", "task_complete", {"reason": "<reason>"}),
        )

        # Add commands to the PromptGenerator object
        for command_label, command_name, args in commands:
            prompt_generator.add_command(command_label, command_name, args)

        # Add resources to the PromptGenerator object
        prompt_generator.add_resource(
            "Internet access for searches and information gathering."
        )
        prompt_generator.add_resource("Long Term memory management.")
        prompt_generator.add_resource(
            "GPT-3.5 powered Agents for delegation of simple tasks."
        )
        prompt_generator.add_resource("File output.")

        # Add performance evaluations to the PromptGenerator object
        prompt_generator.add_performance_evaluation(
            "Continuously review and analyze your actions to ensure you are performing to"
            " the best of your abilities."
        )
        prompt_generator.add_performance_evaluation(
            "Constructively self-criticize your big-picture behavior constantly."
        )
        prompt_generator.add_performance_evaluation(
            "Reflect on past decisions and strategies to refine your approach."
        )
        prompt_generator.add_performance_evaluation(
            "Every command has a cost, so be smart and efficient. Aim to complete tasks in"
            " the least number of steps."
        )

        # Generate the prompt string
        return prompt_generator.generate_prompt_string()
