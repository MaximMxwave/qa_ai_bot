from aiogram import Dispatcher
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import logging
from messages import WELCOME_MSG, MENU_MSG, HELP_MSG, get_main_menu, get_back_menu
from config import Config

logger = logging.getLogger(__name__)

# Импорты команд
from plugins.json_validator import (
    json_validator_command,
    process_json_validation,
    process_repeat_choice,
    JsonValidatorStates
)

from plugins.file_generator import (
    generate_file_command,
    process_format_choice,
    process_file_params,
    handle_choice,
    FileGeneratorStates
)

from plugins.payment_generator import (
    generate_payment_command as payment_gen_command,
    process_payment_system,
    process_regenerate_choice,
    PaymentGeneratorStates
)

from plugins.pairwise_tester import (
    pairwise_command as pairwise_test_command,
    process_pairwise_parameters,
    PairwiseStates
)

from plugins.test_case_template import (
    test_case_template_command,
    process_title,
    process_description,
    process_preconditions,
    process_steps,
    process_expected_result,
    process_priority,
    handle_choice as test_case_handle_choice,
    TestCaseTemplateStates
)

from plugins.bug_report_creator import (
    bug_report_command,
    process_bug_title,
    process_bug_description,
    process_bug_steps,
    process_bug_actual_result,
    process_bug_expected_result,
    process_bug_environment,
    process_bug_severity,
    process_bug_logs,
    process_bug_curl,
    process_bug_docs,
    handle_choice as bug_report_handle_choice,
    BugReportStates
)

from plugins.test_data_generator import (
    generate_test_data_command,
    process_count,
    process_regenerate_choice,
    TestDataGeneratorStates
)

class CommandRouter:
    def __init__(self, dp: Dispatcher):
        self.dp = dp
        self.text_commands = {
            "🗂 создать файл": self.handle_file_command,
            "💳 создать банковскую карту": self.handle_payment_command,
            "🧪 создать pairwise тест": self.handle_pairwise_command,
            "📑 проверить json": self.handle_json_validator_command,
            "📋 создать тест-кейс": self.handle_test_case_template_command,
            "🐞 создать баг-репорт": self.handle_bug_report_command,
            "👥 создать тестовые данные": self.handle_test_data_command,
            "назад в меню": self.handle_back_to_menu,
            "информация": self.handle_help_command
        }

    async def handle_json_validator_command(self, message: Message, state: FSMContext):
        await state.clear()
        await state.set_state(JsonValidatorStates.waiting_for_json)
        await json_validator_command(message, state)

    async def handle_file_command(self, message: Message, state: FSMContext):
        await state.clear()
        await state.set_state(FileGeneratorStates.waiting_for_format)
        await generate_file_command(message, state)

    async def handle_payment_command(self, message: Message, state: FSMContext):
        await state.clear()
        await state.set_state(PaymentGeneratorStates.waiting_for_payment_system)
        await payment_gen_command(message, state)

    async def handle_pairwise_command(self, message: Message, state: FSMContext):
        await state.clear()
        await state.set_state(PairwiseStates.waiting_for_parameters)
        await pairwise_test_command(message, state)

    async def handle_test_case_template_command(self, message: Message, state: FSMContext):
        await state.clear()
        await state.set_state(TestCaseTemplateStates.waiting_for_title)
        await test_case_template_command(message, state)

    async def handle_bug_report_command(self, message: Message, state: FSMContext):
        await state.clear()
        await state.set_state(BugReportStates.waiting_for_title)
        await bug_report_command(message, state)

    async def handle_test_data_command(self, message: Message, state: FSMContext):
        await state.clear()
        await state.set_state(TestDataGeneratorStates.waiting_for_count)
        await generate_test_data_command(message, state)

    async def handle_back_to_menu(self, message: Message, state: FSMContext):
        await state.clear()
        await message.answer(MENU_MSG, reply_markup=get_main_menu())

    async def handle_help_command(self, message: Message, state: FSMContext):
        await state.clear()
        await message.answer(HELP_MSG, reply_markup=get_main_menu())

    def register_handlers(self):
        try:
            logger.info("Регистрация обработчиков команд...")
            
            # Универсальный обработчик /cancel
            @self.dp.message(Command("cancel"))
            async def cmd_cancel(message: Message, state: FSMContext):
                await state.clear()
                await message.answer("✅ Операция отменена", reply_markup=get_main_menu())

            # Обработчики базовых команд
            @self.dp.message(Command("start"))
            async def cmd_start(message: Message, state: FSMContext):
                await state.clear()
                await message.answer(WELCOME_MSG, reply_markup=get_main_menu())

            @self.dp.message(Command("help"))
            async def cmd_help(message: Message, state: FSMContext):
                await self.handle_help_command(message, state)

            # Обработчики специализированных команд
            @self.dp.message(Command("file"))
            async def cmd_genfile(message: Message, state: FSMContext):
                await self.handle_file_command(message, state)

            @self.dp.message(Command("payment"))
            async def cmd_genpayment(message: Message, state: FSMContext):
                await self.handle_payment_command(message, state)

            @self.dp.message(Command("pairwise"))
            async def cmd_pairwise(message: Message, state: FSMContext):
                await self.handle_pairwise_command(message, state)
            
            @self.dp.message(Command("json"))
            async def cmd_validatejson(message: Message, state: FSMContext):
                await self.handle_json_validator_command(message, state)
            
            @self.dp.message(Command("testcase"))
            async def cmd_testcase(message: Message, state: FSMContext):
                await self.handle_test_case_template_command(message, state)

            @self.dp.message(Command("bug"))
            async def cmd_bug(message: Message, state: FSMContext):
                await self.handle_bug_report_command(message, state)

            @self.dp.message(Command("testdata"))
            async def cmd_testdata(message: Message, state: FSMContext):
                await self.handle_test_data_command(message, state)

            # Обработчики состояний с проверкой /help
            @self.dp.message(StateFilter(FileGeneratorStates.waiting_for_format))
            async def handle_format_choice(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                await process_format_choice(message, state)
            
            @self.dp.message(StateFilter(FileGeneratorStates.waiting_for_params))
            async def handle_file_state(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                if message.text == "Назад в меню":
                    await self.handle_back_to_menu(message, state)
                    return
                await process_file_params(message, state)
                    
            @self.dp.message(StateFilter(FileGeneratorStates.waiting_for_choice))
            async def handle_file_choice(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                await handle_choice(message, state)
          
            @self.dp.message(StateFilter(PaymentGeneratorStates.waiting_for_payment_system))
            async def handle_payment_state(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                if message.text == "Назад в меню":
                    await self.handle_back_to_menu(message, state)
                    return
                await process_payment_system(message, state)

            @self.dp.message(StateFilter(PaymentGeneratorStates.waiting_for_regenerate_choice))
            async def handle_regenerate_choice(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                if message.text == "Назад в меню":
                    await self.handle_back_to_menu(message, state)
                    return
                await process_regenerate_choice(message, state)

            @self.dp.message(StateFilter(PairwiseStates.waiting_for_parameters))
            async def handle_pairwise_state(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                if message.text == "Назад в меню":
                    await self.handle_back_to_menu(message, state)
                    return
                await process_pairwise_parameters(message, state)

            @self.dp.message(StateFilter(PairwiseStates.waiting_for_action))
            async def handle_pairwise_action(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                from plugins.pairwise_tester import process_pairwise_action
                await process_pairwise_action(message, state)

            @self.dp.message(StateFilter(JsonValidatorStates.waiting_for_json))
            async def handle_json_validation(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                if message.text == "Назад в меню":
                    await self.handle_back_to_menu(message, state)
                    return
                await process_json_validation(message, state)
          
            @self.dp.message(StateFilter(JsonValidatorStates.waiting_for_repeat))
            async def handle_json_repeat_choice(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                if message.text == "Назад в меню":
                    await self.handle_back_to_menu(message, state)
                    return
                await process_repeat_choice(message, state)

            @self.dp.message(StateFilter(TestCaseTemplateStates.waiting_for_title))
            async def handle_test_case_title(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                if message.text == "Назад в меню":
                    await self.handle_back_to_menu(message, state)
                    return
                await process_title(message, state)

            @self.dp.message(StateFilter(TestCaseTemplateStates.waiting_for_description))
            async def handle_test_case_description(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                if message.text == "Назад в меню":
                    await self.handle_back_to_menu(message, state)
                    return
                await process_description(message, state)

            @self.dp.message(StateFilter(TestCaseTemplateStates.waiting_for_preconditions))
            async def handle_test_case_preconditions(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                if message.text == "Назад в меню":
                    await self.handle_back_to_menu(message, state)
                    return
                await process_preconditions(message, state)

            @self.dp.message(StateFilter(TestCaseTemplateStates.waiting_for_steps))
            async def handle_test_case_steps(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                if message.text == "Назад в меню":
                    await self.handle_back_to_menu(message, state)
                    return
                await process_steps(message, state)

            @self.dp.message(StateFilter(TestCaseTemplateStates.waiting_for_expected_result))
            async def handle_test_case_expected_result(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                if message.text == "Назад в меню":
                    await self.handle_back_to_menu(message, state)
                    return
                await process_expected_result(message, state)

            @self.dp.message(StateFilter(TestCaseTemplateStates.waiting_for_priority))
            async def handle_test_case_priority(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                if message.text == "Назад в меню":
                    await self.handle_back_to_menu(message, state)
                    return
                await process_priority(message, state)

            @self.dp.message(StateFilter(TestCaseTemplateStates.waiting_for_choice))
            async def handle_test_case_choice(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                await test_case_handle_choice(message, state)

            @self.dp.message(StateFilter(BugReportStates.waiting_for_title))
            async def handle_bug_title(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                if message.text == "Назад в меню":
                    await self.handle_back_to_menu(message, state)
                    return
                await process_bug_title(message, state)

            @self.dp.message(StateFilter(BugReportStates.waiting_for_description))
            async def handle_bug_description(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                if message.text == "Назад в меню":
                    await self.handle_back_to_menu(message, state)
                    return
                await process_bug_description(message, state)

            @self.dp.message(StateFilter(BugReportStates.waiting_for_steps))
            async def handle_bug_steps(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                if message.text == "Назад в меню":
                    await self.handle_back_to_menu(message, state)
                    return
                await process_bug_steps(message, state)

            @self.dp.message(StateFilter(BugReportStates.waiting_for_actual_result))
            async def handle_bug_actual_result(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                if message.text == "Назад в меню":
                    await self.handle_back_to_menu(message, state)
                    return
                await process_bug_actual_result(message, state)

            @self.dp.message(StateFilter(BugReportStates.waiting_for_expected_result))
            async def handle_bug_expected_result(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                if message.text == "Назад в меню":
                    await self.handle_back_to_menu(message, state)
                    return
                await process_bug_expected_result(message, state)

            @self.dp.message(StateFilter(BugReportStates.waiting_for_environment))
            async def handle_bug_environment(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                if message.text == "Назад в меню":
                    await self.handle_back_to_menu(message, state)
                    return
                await process_bug_environment(message, state)

            @self.dp.message(StateFilter(BugReportStates.waiting_for_severity))
            async def handle_bug_severity(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                if message.text == "Назад в меню":
                    await self.handle_back_to_menu(message, state)
                    return
                await process_bug_severity(message, state)

            @self.dp.message(StateFilter(BugReportStates.waiting_for_logs))
            async def handle_bug_logs(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                if message.text == "Назад в меню":
                    await self.handle_back_to_menu(message, state)
                    return
                await process_bug_logs(message, state)

            @self.dp.message(StateFilter(BugReportStates.waiting_for_curl))
            async def handle_bug_curl(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                if message.text == "Назад в меню":
                    await self.handle_back_to_menu(message, state)
                    return
                await process_bug_curl(message, state)

            @self.dp.message(StateFilter(BugReportStates.waiting_for_docs))
            async def handle_bug_docs(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                if message.text == "Назад в меню":
                    await self.handle_back_to_menu(message, state)
                    return
                await process_bug_docs(message, state)

            @self.dp.message(StateFilter(BugReportStates.waiting_for_choice))
            async def handle_bug_choice(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                await bug_report_handle_choice(message, state)

            @self.dp.message(StateFilter(TestDataGeneratorStates.waiting_for_count))
            async def handle_test_data_count(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                if message.text == "Назад в меню":
                    await self.handle_back_to_menu(message, state)
                    return
                await process_count(message, state)

            @self.dp.message(StateFilter(TestDataGeneratorStates.waiting_for_regenerate_choice))
            async def handle_test_data_regenerate_choice(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                if message.text == "Назад в меню":
                    await self.handle_back_to_menu(message, state)
                    return
                await process_regenerate_choice(message, state)

            # Главный обработчик текстовых сообщений
            @self.dp.message()
            async def handle_text(message: Message, state: FSMContext):
                text = message.text.lower()
                if text in self.text_commands:
                    await self.text_commands[text](message, state)
                else:
                    current_state = await state.get_state()
                    if not current_state:
                        await message.answer(MENU_MSG, reply_markup=get_main_menu())

            logger.info("Все обработчики успешно зарегистрированы")
            
        except Exception as e:
            logger.error(f"Ошибка регистрации обработчиков: {e}", exc_info=True)
            raise



# AI Model Selection (NEW!)
async def ask_for_ai_model(message: Message) -> str:
    """Ask user to select AI model"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔴 OpenAI GPT")],
            [KeyboardButton(text="⚫ Claude")],
            [KeyboardButton(text="🟦 DeepSeek")],
            [KeyboardButton(text="❌ No AI")]
        ],
        resize_keyboard=True
    )
    
    await message.answer(
        "🤖 <b>Choose AI assistant for help:</b>\n\n"
        "🔴 <b>OpenAI GPT</b> - Fast and powerful\n"
        "⚫ <b>Claude</b> - Detailed analysis\n"
        "🟦 <b>DeepSeek</b> - Quick answers\n"
        "❌ <b>No AI</b> - Standard mode",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
