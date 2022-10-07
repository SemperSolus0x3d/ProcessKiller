from psutil import Process

class ProcessKillService:
    def kill_processes(self, processes: list[Process]):
        for process in processes:
            process.kill()
            print(f'Killed {process.name()} process')
