import Assistant_Experimental.config.SysConf as S_config
import Assistant_Experimental.config.libConfig as Lib_conf

System = {}
System.update(S_config.System)

Libraries = {'tele_bot': {}}
Libraries['tele_bot'].update(Lib_conf.bot_conf)
