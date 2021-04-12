from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Serene Visage"

def sereneVisageSpellBonusToBluff(attachee, args, evt_obj):
    evt_obj.bonus_list.add(args.get_arg(2), 18, "~Serene Visage~[TAG_SPELLS_SERENE_VISAGE] ~Insight~[TAG_MODIFIER_INSIGHT] Bonus") #Insight bonus value is passed from casting script
    return 0

def sereneVisageSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Serene Visage (" + str(args.get_arg(1)) + " round)")
    else:
        evt_obj.append("Serene Visage (" + str(args.get_arg(1)) + " rounds)")
    return 0

def sereneVisageSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("SERENE_VISAGE"), -2, " (" + str(args.get_arg(1)) + " round)")
    else:
        evt_obj.append(tpdp.hash("SERENE_VISAGE"), -2, " (" + str(args.get_arg(1)) + " rounds)")
    return 0

def sereneVisageSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0
    
def sereneVisageSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def sereneVisageSpellSpellEnd(attachee, args, evt_obj):
    print "Serene Visage SpellEnd"
    return 0

sereneVisageSpell = PythonModifier("sp-Serene Visage", 3) # spell_id, duration, bonusToBluff
sereneVisageSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_BLUFF, sereneVisageSpellBonusToBluff,())
sereneVisageSpell.AddHook(ET_OnGetTooltip, EK_NONE, sereneVisageSpellTooltip, ())
sereneVisageSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, sereneVisageSpellEffectTooltip, ())
sereneVisageSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, sereneVisageSpellSpellEnd, ())
sereneVisageSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, sereneVisageSpellHasSpellActive, ())
sereneVisageSpell.AddHook(ET_OnD20Signal, EK_S_Killed, sereneVisageSpellKilled, ())
sereneVisageSpell.AddSpellDispelCheckStandard()
sereneVisageSpell.AddSpellTeleportPrepareStandard()
sereneVisageSpell.AddSpellTeleportReconnectStandard()
sereneVisageSpell.AddSpellCountdownStandardHook()
