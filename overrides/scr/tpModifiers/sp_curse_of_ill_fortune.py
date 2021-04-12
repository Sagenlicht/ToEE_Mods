from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Curse of Ill Fortune"

def curseOfIllFortuneSpellPenalty(attachee, args, evt_obj):
    evt_obj.bonus_list.add(-3, 0, "~Curse of Ill Fortune~[TAG_SPELLS_CURSE_OF_ILL_FORTUNE] penalty") #Curse gives -3 on attack rolls, saves, ability checks and skill checks
    return 0

def curseOfIllFortuneSpellCheckRemoveBySpell(attachee, args, evt_obj): #not tested what happens if spell gets interrupted
    spellToCheck = tpdp.SpellPacket(evt_obj.data1)
    spellsThatRemoveCurse = [spell_break_enchantment, spell_remove_curse, spell_miracle, spell_wish]
    if spellToCheck.spell_enum in spellsThatRemoveCurse:
        args.remove_spell()
        args.remove_spell_mod()
    return 0

def curseOfIllFortuneSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Curse of Ill Fortune ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Curse of Ill Fortune ({} rounds)".format(args.get_arg(1)))
    return 0

def curseOfIllFortuneSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("CURSE_OF_ILL_FORTUNE"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("CURSE_OF_ILL_FORTUNE"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def curseOfIllFortuneSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def curseOfIllFortuneSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def curseOfIllFortuneSpellSpellEnd(attachee, args, evt_obj):
    print "Curse of Ill FortuneSpellEnd"
    return 0

curseOfIllFortuneSpell = PythonModifier("sp-Curse of Ill Fortune", 2) # spell_id, duration
curseOfIllFortuneSpell.AddHook(ET_OnToHitBonus2, EK_NONE, curseOfIllFortuneSpellPenalty,())
curseOfIllFortuneSpell.AddHook(ET_OnSaveThrowLevel, EK_NONE, curseOfIllFortuneSpellPenalty,())
curseOfIllFortuneSpell.AddHook(ET_OnGetAbilityCheckModifier, EK_NONE, curseOfIllFortuneSpellPenalty,())
curseOfIllFortuneSpell.AddHook(ET_OnGetSkillLevel, EK_NONE, curseOfIllFortuneSpellPenalty,())
curseOfIllFortuneSpell.AddHook(ET_OnD20Signal, EK_S_Spell_Cast, curseOfIllFortuneSpellCheckRemoveBySpell, ())
curseOfIllFortuneSpell.AddHook(ET_OnGetTooltip, EK_NONE, curseOfIllFortuneSpellTooltip, ())
curseOfIllFortuneSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, curseOfIllFortuneSpellEffectTooltip, ())
curseOfIllFortuneSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, curseOfIllFortuneSpellSpellEnd, ())
curseOfIllFortuneSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, curseOfIllFortuneSpellHasSpellActive, ())
curseOfIllFortuneSpell.AddHook(ET_OnD20Signal, EK_S_Killed, curseOfIllFortuneSpellKilled, ())
curseOfIllFortuneSpell.AddSpellTeleportPrepareStandard()
curseOfIllFortuneSpell.AddSpellTeleportReconnectStandard()
curseOfIllFortuneSpell.AddSpellCountdownStandardHook()
