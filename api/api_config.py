from pathlib import Path
import sys

sys.path.append(Path(__file__).parents[1].absolute())

import config.sys_conf as S_config
import config.lib_config as Lib_conf
import config.help_config as Help_conf

System = S_config.System
Libraries = {'tele_bot': Lib_conf.bot_conf}
Helpers = {'parser': Help_conf.parser}
DB = S_config.Db
