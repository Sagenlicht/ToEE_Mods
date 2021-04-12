from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Insidious Rhythm"

def insidiousRhythmSpellPenaltyToSkills(attachee, args, evt_obj):
    evt_obj.bonus_list.add(-4, 0, "~Insidious Rhythm~[TAG_SPELLS_INSIDIOUS_RHYTHM] Penalty") #Insidious Rhythm is a -4 penalty on intelligence based skills and Concentration
    return 0

def insidiousRhythmSpellGetSpellLevel(attachee, args, evt_obj):
    spellPacket = evt_obj.get_spell_packet()
    spellLevel = spellPacket.spell_known_slot_level #not tested with metamagic hightend spells
    args.set_arg(3, spellLevel)
    return 0

def insidiousRhythmSpellConcentrationCheck(attachee, args, evt_obj):
    attachee.float_text_line("Concentration Check", tf_red)
    skillCheckDc = args.get_arg(2) + args.get_arg(3) # spellDC + spellLevel
    concentrationSkillValue = attachee.skill_level_get(skill_concentration)
    if concentrationSkillValue == OBJ_HANDLE_NULL:
        concentrationSkillValue = 0
    skillDice = dice_new('1d20')
    skillDiceRoll = skillDice.roll()
    skillRollResult = skillDiceRoll + concentrationSkillValue
    game.create_history_freeform(attachee.description + " attempts a ~Insidious Rhythm~[TAG_SPELLS_INSIDIOUS_RHYTHM] concenatration check (DC{}): \n\n".format(skillCheckDc))
    if skillRollResult < skillCheckDc:
        attachee.float_text_line("failed", tf_red)
        game.create_history_freeform("Rolled a ({}) - Failure! \n\n".format(skillRollResult))
        game.particles('Fizzle', attachee)
        evt_obj.return_val = 100
    else:
        attachee.float_text_line("success")
        game.create_history_freeform("Rolled a ({}) - Success! \n\n".format(skillRollResult))
    return 0

def insidiousRhythmSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Insidious Rhythm ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Insidious Rhythm ({} rounds)".format(args.get_arg(1)))
    return 0

def insidiousRhythmSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("INSIDIOUS_RHYTHM"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("INSIDIOUS_RHYTHM"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def insidiousRhythmSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def insidiousRhythmSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def insidiousRhythmSpellSpellEnd(attachee, args, evt_obj):
    print "Insidious Rhythm SpellEnd"
    return 0

insidiousRhythmSpell = PythonModifier("sp-Insidious Rhythm", 4) # spell_id, duration, spellDc, spellLevel
insidiousRhythmSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_CONCENTRATION, insidiousRhythmSpellPenaltyToSkills,())
insidiousRhythmSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_APPRAISE, insidiousRhythmSpellPenaltyToSkills,())
insidiousRhythmSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_DISABLE_DEVICE, insidiousRhythmSpellPenaltyToSkills,())
insidiousRhythmSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_SEARCH, insidiousRhythmSpellPenaltyToSkills,())
insidiousRhythmSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_SPELLCRAFT, insidiousRhythmSpellPenaltyToSkills,())
insidiousRhythmSpell.AddHook(ET_OnGetCasterLevelMod, EK_NONE, insidiousRhythmSpellGetSpellLevel, ())
insidiousRhythmSpell.AddHook(ET_OnD20Query, EK_Q_SpellInterrupted, insidiousRhythmSpellConcentrationCheck,())
insidiousRhythmSpell.AddHook(ET_OnGetTooltip, EK_NONE, insidiousRhythmSpellTooltip, ())
insidiousRhythmSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, insidiousRhythmSpellEffectTooltip, ())
insidiousRhythmSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, insidiousRhythmSpellSpellEnd, ())
insidiousRhythmSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, insidiousRhythmSpellHasSpellActive, ())
insidiousRhythmSpell.AddHook(ET_OnD20Signal, EK_S_Killed, insidiousRhythmSpellKilled, ())
insidiousRhythmSpell.AddSpellDispelCheckStandard()
insidiousRhythmSpell.AddSpellTeleportPrepareStandard()
insidiousRhythmSpell.AddSpellTeleportReconnectStandard()
insidiousRhythmSpell.AddSpellCountdownStandardHook()
