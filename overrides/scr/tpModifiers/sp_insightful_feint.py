from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Insightful Feint"

def insightfulFeintSpellBonus(attachee, args, evt_obj):
    #Needs a check, so its only added if used to feint, but I haven't found a working one yet, limiting it to combat for now, which should block usage for dialogues which is enough.
    if game.combat_is_active():
        evt_obj.bonus_list.add(10, 18, "~Insightful Feint~[TAG_SPELL_INSIGHTFUL_FEINT] Insight Bonus") #Insightful Feint adds a +10 Insight Bonus to next Feint Check
    return 0

def insightfulFeintSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Insightful Feint ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Insightful Feint ({} rounds)".format(args.get_arg(1)))
    return 0

def insightfulFeintSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("INSIGHTFUL_FEINT"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("INSIGHTFUL_FEINT"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def insightfulFeintSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def insightfulFeintSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def insightfulFeintSpellSpellEnd(attachee, args, evt_obj):
    print "Insightful Feint SpellEnd"
    return 0

insightfulFeintSpell = PythonModifier("sp-Insightful Feint", 2) # spell_id, duration
insightfulFeintSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_BLUFF, insightfulFeintSpellBonus,())
insightfulFeintSpell.AddHook(ET_OnGetTooltip, EK_NONE, insightfulFeintSpellTooltip, ())
insightfulFeintSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, insightfulFeintSpellEffectTooltip, ())
insightfulFeintSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, insightfulFeintSpellSpellEnd, ())
insightfulFeintSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, insightfulFeintSpellHasSpellActive, ())
insightfulFeintSpell.AddHook(ET_OnD20Signal, EK_S_Killed, insightfulFeintSpellKilled, ())
insightfulFeintSpell.AddSpellDispelCheckStandard()
insightfulFeintSpell.AddSpellTeleportPrepareStandard()
insightfulFeintSpell.AddSpellTeleportReconnectStandard()
insightfulFeintSpell.AddSpellCountdownStandardHook()
