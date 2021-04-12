from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Wraithstrike"

def wraithstrikeSpellAddTouchFlag(attachee, args, evt_obj):
    if not evt_obj.attack_packet.get_flags() & D20CAF_TOUCH_ATTACK:
        #evt_obj.attack_packet.set_flags(D20CAF_TOUCH_ATTACK) #does not work :(
        evt_obj.bonus_list.add_cap(9 , 0, 1, "~Wraithstrike~[TAG_SPELLS_WRAITHSTRIKE]")
        evt_obj.bonus_list.add_cap(10 , 0, 1, "~Wraithstrike~[TAG_SPELLS_WRAITHSTRIKE]")
        evt_obj.bonus_list.add_cap(28 , 0, 1, "~Wraithstrike~[TAG_SPELLS_WRAITHSTRIKE]")
        evt_obj.bonus_list.add_cap(29 , 0, 1, "~Wraithstrike~[TAG_SPELLS_WRAITHSTRIKE]")
        evt_obj.bonus_list.add_cap(33 , 0, 1, "~Wraithstrike~[TAG_SPELLS_WRAITHSTRIKE]")
    return 0

def wraithstrikeSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Wraithstrike ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Wraithstrike ({} rounds)".format(args.get_arg(1)))
    return 0

def wraithstrikeSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("WRAITHSTRIKE"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("WRAITHSTRIKE"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def wraithstrikeSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def wraithstrikeSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def wraithstrikeSpellSpellEnd(attachee, args, evt_obj):
    print "Wraithstrike SpellEnd"
    return 0

wraithstrikeSpell = PythonModifier("sp-Wraithstrike", 2) # spell_id, duration
wraithstrikeSpell.AddHook(ET_OnGetAcModifierFromAttacker, EK_NONE, wraithstrikeSpellAddTouchFlag,())
wraithstrikeSpell.AddHook(ET_OnGetTooltip, EK_NONE, wraithstrikeSpellTooltip, ())
wraithstrikeSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, wraithstrikeSpellEffectTooltip, ())
wraithstrikeSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, wraithstrikeSpellSpellEnd, ())
wraithstrikeSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, wraithstrikeSpellHasSpellActive, ())
wraithstrikeSpell.AddHook(ET_OnD20Signal, EK_S_Killed, wraithstrikeSpellKilled, ())
wraithstrikeSpell.AddSpellDispelCheckStandard()
wraithstrikeSpell.AddSpellTeleportPrepareStandard()
wraithstrikeSpell.AddSpellTeleportReconnectStandard()
wraithstrikeSpell.AddSpellCountdownStandardHook()
