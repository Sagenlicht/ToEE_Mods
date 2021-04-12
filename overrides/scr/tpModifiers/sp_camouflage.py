from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Camouflage"

def camouflageSpellBonusToHide(attachee, args, evt_obj):
    evt_obj.bonus_list.add(10, 21, "~Camouflage~[TAG_SPELLS_CAMOUFLAGE] ~Circumstance~[TAG_MODIFIER_CIRCUMSTANCE] Bonus") # Camouflage is a flat +10 circumstance bouns to hide
    return 0

def camouflageSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Camouflage ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Camouflage ({} rounds)".format(args.get_arg(1)))
    return 0

def camouflageSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("CAMOUFLAGE"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("CAMOUFLAGE"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def camouflageSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def camouflageSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def camouflageSpellSpellEnd(attachee, args, evt_obj):
    print "Camouflage SpellEnd"
    return 0

camouflageSpell = PythonModifier("sp-Camouflage", 2) # spell_id, duration
camouflageSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_HIDE, camouflageSpellBonusToHide,())
camouflageSpell.AddHook(ET_OnGetTooltip, EK_NONE, camouflageSpellTooltip, ())
camouflageSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, camouflageSpellEffectTooltip, ())
camouflageSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, camouflageSpellSpellEnd, ())
camouflageSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, camouflageSpellHasSpellActive, ())
camouflageSpell.AddHook(ET_OnD20Signal, EK_S_Killed, camouflageSpellKilled, ())
camouflageSpell.AddSpellDispelCheckStandard()
camouflageSpell.AddSpellTeleportPrepareStandard()
camouflageSpell.AddSpellTeleportReconnectStandard()
camouflageSpell.AddSpellCountdownStandardHook()
