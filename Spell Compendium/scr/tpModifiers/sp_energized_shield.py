from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
import spell_utils
print "Registering sp-Energized Shield"

energizedShieldSpell = PythonModifier("sp-Energized Shield", 2) # spell_id, duration
energizedShieldSpell.AddHook(ET_OnGetTooltip, EK_NONE, spell_utils.spellTooltip, ())
energizedShieldSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, spell_utils.spellEffectTooltip, ())
energizedShieldSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, spell_utils.queryActiveSpell, ())
energizedShieldSpell.AddHook(ET_OnD20Signal, EK_S_Killed, spell_utils.spellKilled, ())
energizedShieldSpell.AddSpellDispelCheckStandard()
energizedShieldSpell.AddSpellTeleportPrepareStandard()
energizedShieldSpell.AddSpellTeleportReconnectStandard()
energizedShieldSpell.AddSpellCountdownStandardHook()
