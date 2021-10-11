from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
import spell_utils
print "Registering sp-Wraithstrike"

def wraithstrikeSpellAddTouchFlag(attachee, args, evt_obj):
    if not evt_obj.attack_packet.get_flags() & D20CAF_TOUCH_ATTACK:
        flags = evt_obj.attack_packet.get_flags()
        flags |= D20CAF_TOUCH_ATTACK
        evt_obj.attack_packet.set_flags(flags)
        #evt_obj.bonus_list.add_cap(9 , 0, 1, "~Wraithstrike~[TAG_SPELLS_WRAITHSTRIKE]")
        #evt_obj.bonus_list.add_cap(10 , 0, 1, "~Wraithstrike~[TAG_SPELLS_WRAITHSTRIKE]")
        #evt_obj.bonus_list.add_cap(28 , 0, 1, "~Wraithstrike~[TAG_SPELLS_WRAITHSTRIKE]")
        #evt_obj.bonus_list.add_cap(29 , 0, 1, "~Wraithstrike~[TAG_SPELLS_WRAITHSTRIKE]")
        #evt_obj.bonus_list.add_cap(33 , 0, 1, "~Wraithstrike~[TAG_SPELLS_WRAITHSTRIKE]")
    return 0

# Swift spells with a current round duration do not need a duplicate check
wraithstrikeSpell = PythonModifier("sp-Wraithstrike", 3) # spell_id, duration, empty
#wraithstrikeSpell.AddHook(ET_OnGetAcModifierFromAttacker, EK_NONE, wraithstrikeSpellAddTouchFlag,())
wraithstrikeSpell.AddHook(ET_OnToHitBonus2, EK_NONE, wraithstrikeSpellAddTouchFlag,())
wraithstrikeSpell.AddHook(ET_OnGetTooltip, EK_NONE, spell_utils.spellTooltip, ())
wraithstrikeSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, spell_utils.spellEffectTooltip, ())
wraithstrikeSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, spell_utils.queryActiveSpell, ())
wraithstrikeSpell.AddHook(ET_OnD20Signal, EK_S_Killed, spell_utils.spellKilled, ())
wraithstrikeSpell.AddSpellDispelCheckStandard()
wraithstrikeSpell.AddSpellTeleportPrepareStandard()
wraithstrikeSpell.AddSpellTeleportReconnectStandard()
wraithstrikeSpell.AddSpellCountdownStandardHook()

