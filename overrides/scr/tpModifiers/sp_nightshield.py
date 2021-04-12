from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Nightshield"

def nightshieldSpellBonusToSaves(attachee, args, evt_obj):
    evt_obj.bonus_list.add(args.get_arg(2), 15, "~Nightshield~[TAG_SPELLS_NIGHTSHIELD] ~Resistance~[TAG_MODIFIER_RESISTANCE] Bonus") #Bonus is passed by spell
    return 0


def nightshieldSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Nightshield ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Nightshield ({} rounds)".format(args.get_arg(1)))
    return 0

def nightshieldSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("NIGHTSHIELD"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("NIGHTSHIELD"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def nightshieldSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    if evt_obj.data1 == spell_shield: #replies to query as spell_shield as well to grant Magic Missile immunity
        evt_obj.return_val = 1
    return 0

def nightshieldSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def nightshieldSpellSpellEnd(attachee, args, evt_obj):
    print "Nightshield SpellEnd"
    return 0

nightshieldSpell = PythonModifier("sp-Nightshield", 3) # spell_id, duration, spellBonus
nightshieldSpell.AddHook(ET_OnSaveThrowLevel, EK_NONE, nightshieldSpellBonusToSaves, ())
nightshieldSpell.AddHook(ET_OnGetTooltip, EK_NONE, nightshieldSpellTooltip, ())
nightshieldSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, nightshieldSpellEffectTooltip, ())
nightshieldSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, nightshieldSpellSpellEnd, ())
nightshieldSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, nightshieldSpellHasSpellActive, ())
nightshieldSpell.AddHook(ET_OnD20Signal, EK_S_Killed, nightshieldSpellKilled, ())
nightshieldSpell.AddSpellDispelCheckStandard()
nightshieldSpell.AddSpellTeleportPrepareStandard()
nightshieldSpell.AddSpellTeleportReconnectStandard()
nightshieldSpell.AddSpellCountdownStandardHook()
