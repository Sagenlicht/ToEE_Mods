from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Strategic Charge"

def strategicChargeSpellFlagAoo(attachee, args, evt_obj):
    args.set_arg(2, 1) #set aooFlag
    return 0

def strategicChargeSpellBonusToAc(attachee, args, evt_obj):
    if args.get_arg(2): #Bonus only granted when attack is an AoO
        attachee.float_text_line("Strategic Charge")
        evt_obj.bonus_list.add(4, 8, "~Mobility~[TAG_Mobility] feat") #Strategic Charge grants the feat Mobilty
        args.set_arg(2, 0) #reset aooFlag
    return 0

def strategicChargeSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Strategic Charge ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Strategic Charge ({} rounds)".format(args.get_arg(1)))
    return 0

def strategicChargeSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("LIGHTFOOT"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("LIGHTFOOT"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def strategicChargeSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def strategicChargeSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def strategicChargeSpellSpellEnd(attachee, args, evt_obj):
    print "Strategic Charge SpellEnd"
    return 0

strategicChargeSpell = PythonModifier("sp-Strategic Charge", 3) # spell_id, duration, aooFlag
strategicChargeSpell.AddHook(ET_OnD20Query, EK_Q_AOOIncurs, strategicChargeSpellFlagAoo,())
strategicChargeSpell.AddHook(ET_OnGetAC, EK_NONE, strategicChargeSpellBonusToAc,())
strategicChargeSpell.AddHook(ET_OnGetTooltip, EK_NONE, strategicChargeSpellTooltip, ())
strategicChargeSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, strategicChargeSpellEffectTooltip, ())
strategicChargeSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, strategicChargeSpellSpellEnd, ())
strategicChargeSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, strategicChargeSpellHasSpellActive, ())
strategicChargeSpell.AddHook(ET_OnD20Signal, EK_S_Killed, strategicChargeSpellKilled, ())
strategicChargeSpell.AddSpellDispelCheckStandard()
strategicChargeSpell.AddSpellTeleportPrepareStandard()
strategicChargeSpell.AddSpellTeleportReconnectStandard()
strategicChargeSpell.AddSpellCountdownStandardHook()
