from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Distract"

def distractSpellPenaltyToSkills(attachee, args, evt_obj):
    evt_obj.bonus_list.add(-4,0,"~Distract~[TAG_SPELLS_DISTRACT] penalty") #Distract gives -4 penalty to Concentration, Listen, Search and Spot checks
    return 0

def distractSpellTurnBasedStatusInit(attachee, args, evt_obj):
    if evt_obj.tb_status.hourglass_state > 2:
        attachee.float_text_line("Distracted", tf_red)
        evt_obj.tb_status.hourglass_state = 2 # Limited to a Standard or Move Action only
    return 0

def distractSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Distract ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Distract ({} rounds)".format(args.get_arg(1)))
    return 0

def distractSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("DISTRACT"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("DISTRACT"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def distractSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0
    
def distractSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def distractSpellSpellEnd(attachee, args, evt_obj):
    print "DistractSpellEnd"
    return 0

distractSpell = PythonModifier("sp-Distract", 2) # spell_id, duration
distractSpell.AddHook(ET_OnTurnBasedStatusInit, EK_NONE, distractSpellTurnBasedStatusInit, ())
distractSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_CONCENTRATION, distractSpellPenaltyToSkills,())
distractSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_LISTEN, distractSpellPenaltyToSkills,())
distractSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_SEARCH, distractSpellPenaltyToSkills,())
distractSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_SPOT, distractSpellPenaltyToSkills,())
distractSpell.AddHook(ET_OnGetTooltip, EK_NONE, distractSpellTooltip, ())
distractSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, distractSpellEffectTooltip, ())
distractSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, distractSpellSpellEnd, ())
distractSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, distractSpellHasSpellActive, ())
distractSpell.AddHook(ET_OnD20Signal, EK_S_Killed, distractSpellKilled, ())
distractSpell.AddSpellDispelCheckStandard()
distractSpell.AddSpellTeleportPrepareStandard()
distractSpell.AddSpellTeleportReconnectStandard()
distractSpell.AddSpellCountdownStandardHook()
