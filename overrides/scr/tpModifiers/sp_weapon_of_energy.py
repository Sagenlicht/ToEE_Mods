from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Weapon of Energy"

def weaponOfEnergySpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Weapon of Energy ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Weapon of Energy ({} rounds)".format(args.get_arg(1)))
    return 0

def weaponOfEnergySpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("WEAPON_OF_ENERGY"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("WEAPON_OF_ENERGY"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def weaponOfEnergySpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def weaponOfEnergySpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def weaponOfEnergySpellSpellEnd(attachee, args, evt_obj):
    print "Weapon of Energy SpellEnd"
    return 0

weaponOfEnergySpell = PythonModifier("sp-Weapon of Energy", 2) # spell_id, duration
weaponOfEnergySpell.AddHook(ET_OnGetTooltip, EK_NONE, weaponOfEnergySpellTooltip, ())
weaponOfEnergySpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, weaponOfEnergySpellEffectTooltip, ())
weaponOfEnergySpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, weaponOfEnergySpellSpellEnd, ())
weaponOfEnergySpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, weaponOfEnergySpellHasSpellActive, ())
weaponOfEnergySpell.AddHook(ET_OnD20Signal, EK_S_Killed, weaponOfEnergySpellKilled, ())
weaponOfEnergySpell.AddSpellDispelCheckStandard()
weaponOfEnergySpell.AddSpellTeleportPrepareStandard()
weaponOfEnergySpell.AddSpellTeleportReconnectStandard()
weaponOfEnergySpell.AddSpellCountdownStandardHook()
