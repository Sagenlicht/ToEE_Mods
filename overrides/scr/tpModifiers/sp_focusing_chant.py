from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Focusing Chant"

def focusingChantSpellBonus(attachee, args, evt_obj):
    evt_obj.bonus_list.add(1,21,"~Focusing Chant~[TAG_SPELLS_FOCUSING_CHANT] ~Circumstance~[TAG_MODIFIER_CIRCUMSTANCE] Bonus") #Focusing Chant adds a +1 Circumstance Bonus to Attack Rolls, Skill and Ability Checks
    return 0

def focusingChantSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Focusing Chant ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Focusing Chant ({} rounds)".format(args.get_arg(1)))
    return 0

def focusingChantSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("FOCUSING_CHANT"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("FOCUSING_CHANT"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def focusingChantSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def focusingChantSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def focusingChantSpellSpellEnd(attachee, args, evt_obj):
    print "Focusing Chant SpellEnd"
    return 0

focusingChantSpell = PythonModifier("sp-Focusing Chant", 2) # spell_id, duration
focusingChantSpell.AddHook(ET_OnToHitBonus2, EK_NONE, focusingChantSpellBonus,())
focusingChantSpell.AddHook(ET_OnGetSkillLevel, EK_NONE, focusingChantSpellBonus,())
focusingChantSpell.AddHook(ET_OnGetAbilityCheckModifier, EK_NONE, focusingChantSpellBonus,())
focusingChantSpell.AddHook(ET_OnGetTooltip, EK_NONE, focusingChantSpellTooltip, ())
focusingChantSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, focusingChantSpellEffectTooltip, ())
focusingChantSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, focusingChantSpellSpellEnd, ())
focusingChantSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, focusingChantSpellHasSpellActive, ())
focusingChantSpell.AddHook(ET_OnD20Signal, EK_S_Killed, focusingChantSpellKilled, ())
focusingChantSpell.AddSpellDispelCheckStandard()
focusingChantSpell.AddSpellTeleportPrepareStandard()
focusingChantSpell.AddSpellTeleportReconnectStandard()
focusingChantSpell.AddSpellCountdownStandardHook()
