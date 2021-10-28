from pathlib import Path
import sys
sys.path.append(Path(__file__).parents[1].absolute())
import config.SysConf as S_config
import config.libConfig as Lib_conf
import config.helpConfig as Help_conf

System = S_config.System
Libraries = {'tele_bot': Lib_conf.bot_conf}
Helpers = {'parser': Help_conf.parser}
