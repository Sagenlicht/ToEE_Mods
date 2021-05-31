from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
import spell_utils
print "Registering sp-Insidious Rhythm"

def insidiousRhythmSpellPenaltyToSkills(attachee, args, evt_obj):
    bonusValue = -4 #Insidious Rhythm is a -4 penalty on intelligence based skills and Concentration
    bonusType = 0 #ID 0 = untyped (stacking)
    evt_obj.bonus_list.add(bonusValue, bonusType, "~Insidious Rhythm~[TAG_SPELLS_INSIDIOUS_RHYTHM] Penalty")
    return 0

def insidiousRhythmSpellGetSpellLevel(attachee, args, evt_obj):
    spellPacket = evt_obj.get_spell_packet()
    spellLevel = spellPacket.spell_known_slot_level #not tested with metamagic hightend spells
    args.set_arg(3, spellLevel)
    return 0

def insidiousRhythmSpellConcentrationCheck(attachee, args, evt_obj):
    skillCheckDc = args.get_arg(2) + args.get_arg(3) # spellDC + spellLevel
    attachee.float_text_line("Concentration Check", tf_red)
    if not spell_utils.skillCheck(attachee, skill_concentration, skillCheckDc):
        attachee.float_text_line("failed", tf_red)
        evt_obj.return_val = 100
    else:
        attachee.float_text_line("success")
    return 0

insidiousRhythmSpell = PythonModifier("sp-Insidious Rhythm", 4) # spell_id, duration, spellDc, spellLevel
insidiousRhythmSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_CONCENTRATION, insidiousRhythmSpellPenaltyToSkills,())
insidiousRhythmSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_APPRAISE, insidiousRhythmSpellPenaltyToSkills,())
insidiousRhythmSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_CRAFT, insidiousRhythmSpellPenaltyToSkills,())
insidiousRhythmSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_DECIPHER_SCRIPT, insidiousRhythmSpellPenaltyToSkills,())
insidiousRhythmSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_DISABLE_DEVICE, insidiousRhythmSpellPenaltyToSkills,())
insidiousRhythmSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_FORGERY, insidiousRhythmSpellPenaltyToSkills,())
insidiousRhythmSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_KNOWLEDGE_ARCANA, insidiousRhythmSpellPenaltyToSkills,())
insidiousRhythmSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_KNOWLEDGE_RELIGION, insidiousRhythmSpellPenaltyToSkills,())
insidiousRhythmSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_KNOWLEDGE_NATURE, insidiousRhythmSpellPenaltyToSkills,())
#insidiousRhythmSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_KNOWLEDGE_ALL, insidiousRhythmSpellPenaltyToSkills,())
insidiousRhythmSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_SEARCH, insidiousRhythmSpellPenaltyToSkills,())
insidiousRhythmSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_SPELLCRAFT, insidiousRhythmSpellPenaltyToSkills,())
insidiousRhythmSpell.AddHook(ET_OnGetCasterLevelMod, EK_NONE, insidiousRhythmSpellGetSpellLevel, ())
insidiousRhythmSpell.AddHook(ET_OnD20Query, EK_Q_SpellInterrupted, insidiousRhythmSpellConcentrationCheck,())
insidiousRhythmSpell.AddHook(ET_OnGetTooltip, EK_NONE, spell_utils.spellTooltip, ())
insidiousRhythmSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, spell_utils.spellEffectTooltip, ())
insidiousRhythmSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, spell_utils.queryActiveSpell, ())
insidiousRhythmSpell.AddHook(ET_OnD20Signal, EK_S_Killed, spell_utils.spellKilled, ())
insidiousRhythmSpell.AddSpellDispelCheckStandard()
insidiousRhythmSpell.AddSpellTeleportPrepareStandard()
insidiousRhythmSpell.AddSpellTeleportReconnectStandard()
insidiousRhythmSpell.AddSpellCountdownStandardHook()
