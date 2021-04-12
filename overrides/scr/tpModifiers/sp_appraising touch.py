from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Appraising Touch"

def appraisingTouchSpellBonus(attachee, args, evt_obj):
    evt_obj.bonus_list.add(10, 18, "~Appraising Touch~[TAG_SPELLS_APPRAISING_TOUCH] ~Insight~[TAG_MODIFIER_INSIGHT] Bonus") #Appraising Touch is a flat +10 insight bouns to Appraise
    return 0

def appraisingTouchSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Appraising Touch ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Appraising Touch ({} rounds)".format(args.get_arg(1)))
    return 0

def appraisingTouchSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("APPRAISING_TOUCH"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("APPRAISING_TOUCH"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def appraisingTouchSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def appraisingTouchSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def appraisingTouchSpellSpellEnd(attachee, args, evt_obj):
    print "appraisingTouchSpellSpellEnd"
    return 0

appraisingTouchSpell = PythonModifier("sp-Appraising Touch", 2) # spell_id, duration
appraisingTouchSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_APPRAISE, appraisingTouchSpellBonus,())
appraisingTouchSpell.AddHook(ET_OnGetTooltip, EK_NONE, appraisingTouchSpellTooltip, ())
appraisingTouchSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, appraisingTouchSpellEffectTooltip, ())
appraisingTouchSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, appraisingTouchSpellSpellEnd, ())
appraisingTouchSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, appraisingTouchSpellHasSpellActive, ())
appraisingTouchSpell.AddHook(ET_OnD20Signal, EK_S_Killed, appraisingTouchSpellKilled, ())
appraisingTouchSpell.AddSpellDispelCheckStandard()
appraisingTouchSpell.AddSpellTeleportPrepareStandard()
appraisingTouchSpell.AddSpellTeleportReconnectStandard()
appraisingTouchSpell.AddSpellCountdownStandardHook()
