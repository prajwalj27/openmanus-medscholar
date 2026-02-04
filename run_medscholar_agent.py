"""
Healthcare Literature Survey Agent Runner

This script provides a command-line interface to run the Healthcare Literature Survey Agent.
It allows users to conduct comprehensive medical and healthcare literature surveys.
"""

import argparse
import asyncio
from typing import Optional

from app.agent.medscholar import MedScholarAgent
from app.logger import logger


async def run_medscholar_agent(prompt: Optional[str] = None):
    """
    Run the Healthcare Literature Survey Agent with a given prompt.

    Args:
        prompt: The research question or topic to survey. If None, prompts user for input.
    """

    agent = MedScholarAgent()

    try:
        if prompt is None:
            print("\n" + "="*80)
            print("Healthcare Literature Survey Agent")
            print("="*80)
            print("\nThis agent will help you conduct comprehensive literature surveys")
            print("on healthcare and medical research topics.\n")
            print("Example topics:")
            print("  - Latest treatments for type 2 diabetes")
            print("  - Effectiveness of telehealth for mental health care")
            print("  - Risk factors for cardiovascular disease in young adults")
            print("  - Machine learning applications in cancer diagnosis")
            print("="*80 + "\n")

            prompt = input("Enter your research question or topic: ")

            if not prompt or not prompt.strip():
                logger.info("No input provided. Exiting.")
                return

            logger.info(f"Starting literature survey on: {prompt}")
            logger.info("This may take several minutes depending on the complexity of the topic...\n")

            # Run the agent
            await agent.run(prompt)

            logger.info("\nLiterature survey completed.")
            logger.info("Please check the workspace directory for the survey report.")

    except KeyboardInterrupt:
        logger.warning("\nSurvey interrupted by user.")
    except Exception as e:
        logger.error(f"An error occurred while running the agent: {e}")
        raise
    finally:
        # Clean up agent resources
        if hasattr(agent, "cleanup"):
            await agent.cleanup()


async def main():
    """
    Main entry point for the MedScholar survey agent.
    """
    parser = argparse.ArgumentParser(
        description="Run Healthcare Literature Survey Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_healthcare_agent.py --prompt "Latest treatments for Alzheimer's disease"
  python run_healthcare_agent.py --topic "COVID-19 vaccine effectiveness"
  python run_healthcare_agent.py  # Interactive mode

The agent will search for relevant literature, analyze sources, and generate
a comprehensive survey report saved to the workspace directory.
        """
    )

    parser.add_argument(
        "--prompt",
        type=str,
        help="Research question or topic for the literature survey"
    )

    parser.add_argument(
        "--topic",
        type=str,
        help="Alias for --prompt: research topic to survey"
    )

    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode (default if no prompt provided)"
    )

    args = parser.parse_args()

    # Determine the prompt to use
    prompt = args.prompt or args.topic

    # Run the survey
    await run_medscholar_agent(prompt)


if __name__ == "__main__":
    asyncio.run(main())

