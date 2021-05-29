from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
import spell_utils
print "Registering sp-Angelskin"

def angelskinSpellEvilDr(attachee, args, evt_obj): 
    evt_obj.damage_packet.add_physical_damage_res(5, D20DAP_UNHOLY, 126) #Angelskin grants DR 5/evil; ID126 in damage.mes is DR
    return 0

angelskinSpell = PythonModifier("sp-Angelskin", 2) # spell_id, duration
angelskinSpell.AddHook(ET_OnTakingDamage , EK_NONE, angelskinSpellEvilDr,())
angelskinSpell.AddHook(ET_OnGetTooltip, EK_NONE, spell_utils.spellTooltip, ())
angelskinSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, spell_utils.spellEffectTooltip, ())
angelskinSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, spell_utils.spellEnd, ())
angelskinSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, spell_utils.queryActiveSpell, ())
angelskinSpell.AddHook(ET_OnD20Signal, EK_S_Killed, spell_utils.spellKilled, ())
angelskinSpell.AddSpellDispelCheckStandard()
angelskinSpell.AddSpellTeleportPrepareStandard()
angelskinSpell.AddSpellTeleportReconnectStandard()
angelskinSpell.AddSpellCountdownStandardHook()
