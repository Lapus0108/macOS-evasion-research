from termcolor import colored

class ResultsDisplayer:
    def show_results(self, results: dict, verbose=False):
        for category, category_results in results.items():
            category_title = "-" * 30 + " " + category + " " + "-" * 30
            print(category_title, '\n')

            if type(category_results) is list:
                self.show_results_list(category_title, category_results, verbose)
            elif type(category_results) is dict:
                self.show_results_dict(category_title, category_results, verbose)

            print('\n')

    def show_results_list(self, category_title: str, category_results: list, verbose: bool):
        failed_checks = 0

        for check in category_results:
            status = check['status']
            if status == 'success':
                result = f"{colored('[VM Detected]', 'red')}" if check['vm_detected'] else f"{colored('[OK]', 'green')}"
                label = f"[{check['label']}]".ljust(len(category_title) - len(result) + 9, '.')
                print(f"{label}{result}")
                if check['vm_detected']:
                    failed_checks += 1
                    if verbose:
                        print(f"  Result: {check['result']}")
            elif status == 'error':
                result = f"{colored('[ERROR]', 'yellow')}"
                label = f"[{check['label']}]".ljust(len(category_title) - len(result) + 9, '.')
                print(f"{label}{result}")
                if verbose:
                    print(f"  Message: {check['error_message']}")

        title = category_title.replace("-", "").strip()
        checks_colored = f"{colored(str(failed_checks), 'red')}" if failed_checks > 0 else f"{colored(str(failed_checks), 'green')}"
        print(f"\n[{title}] Failed: {checks_colored} | Total: {len(category_results)}")

    def show_results_dict(self, category_title: str, category_results: dict, verbose: bool):
        failed_checks = 0

        for category_name, category_items in category_results.items():  
            result = f"{colored('[VM Detected]', 'red')}" if len(category_items) > 0 else f"{colored('[OK]', 'green')}"
            label = f"[{category_name}]".ljust(len(category_title) - len(result) + 9, '.')
            print(f"{label}{result}")
            if len(category_items) > 0:
                failed_checks += 1
            if verbose:
                for item in category_items:
                    print(f"  {item['type'].capitalize()} found: {item['path']}")
        
        title = category_title.replace("-", "").strip()
        checks_colored = f"{colored(str(failed_checks), 'red')}" if failed_checks > 0 else f"{colored(str(failed_checks), 'green')}"
        print(f"\n[{title}] Failed: {checks_colored} | Total: {len(category_results.keys())}")