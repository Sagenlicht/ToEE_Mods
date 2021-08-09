from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
import spell_utils
print "Registering sp-Lightfoot"

def lightfootSpellCancelAoO(attachee, args, evt_obj):
    attachee.float_text_line("Lightfooted")
    evt_obj.return_val = 0
    return 0

#Swift spells with a current round duration do not need a duplicate check
lightfootSpell = PythonModifier("sp-Lightfoot", 3) # spell_id, duration, empty
lightfootSpell.AddHook(ET_OnD20Query, EK_Q_AOOIncurs, lightfootSpellCancelAoO,())
lightfootSpell.AddHook(ET_OnGetTooltip, EK_NONE, spell_utils.spellTooltip, ())
lightfootSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, spell_utils.spellEffectTooltip, ())
lightfootSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, spell_utils.queryActiveSpell, ())
lightfootSpell.AddHook(ET_OnD20Signal, EK_S_Killed, spell_utils.spellKilled, ())
lightfootSpell.AddSpellDispelCheckStandard()
lightfootSpell.AddSpellTeleportPrepareStandard()
lightfootSpell.AddSpellTeleportReconnectStandard()
lightfootSpell.AddSpellCountdownStandardHook()
