from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
import spell_utils
print "Registering sp-Phantom Threat"

def phantomThreatSpellSetFlankedCondition(attachee, args, evt_obj):
    # check if cannot be flanked missing though I am unsure how uncanny dodge works and maybe I do not have to check for it anyways; needs testing
    if evt_obj.attack_packet.get_flags() & D20CAF_FLANKED:
        return 0
    flags = evt_obj.attack_packet.get_flags()
    flags |= D20CAF_FLANKED
    evt_obj.attack_packet.set_flags(flags)
    attachee.float_text_line("Phantom Threat", tf_red)
    #if not evt_obj.attack_packet.get_flags() & D20CAF_RANGED: # does not work :(
    #checks if attacker mainhand weapon has range flag; this does not check for throwables,but throwables can also be use for melee
    if not evt_obj.attack_packet.attacker.item_worn_at(item_wear_weapon_primary).obj_get_int(obj_f_weapon_flags) & OWF_RANGED_WEAPON:
        bonusValue = 2
        bonusType = 0 #ID 0 = untyped (stacking)
        bonusMesId = 201 #ID201 is flanked in bonus.mes
        evt_obj.bonus_list.add(bonusValue, bonusType, bonusMesId)
    return 0

phantomThreatSpell = PythonModifier("sp-Phantom Threat", 3, False) # spell_id, duration, empty
phantomThreatSpell.AddHook(ET_OnToHitBonusFromDefenderCondition, EK_NONE, phantomThreatSpellSetFlankedCondition,())
phantomThreatSpell.AddHook(ET_OnGetTooltip, EK_NONE, spell_utils.spellTooltip, ())
phantomThreatSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, spell_utils.spellEffectTooltip, ())
phantomThreatSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, spell_utils.queryActiveSpell, ())
phantomThreatSpell.AddHook(ET_OnD20Signal, EK_S_Killed, spell_utils.spellKilled, ())
phantomThreatSpell.AddSpellDispelCheckStandard()
phantomThreatSpell.AddSpellTeleportPrepareStandard()
phantomThreatSpell.AddSpellTeleportReconnectStandard()
phantomThreatSpell.AddSpellCountdownStandardHook()
