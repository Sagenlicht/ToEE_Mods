from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
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
    if not evt_obj.attack_packet.attacker.item_worn_at(item_wear_weapon_primary).obj_get_int(obj_f_weapon_flags) & OWF_RANGED_WEAPON: #checks if attacker mainhand weapon has range flag; this does not check for throwables,but throwables can also be use for melee
        evt_obj.bonus_list.add(2, 0, 201) #ID201 is flanked in bonus.mes
    return 0

def phantomThreatSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Phantom Threat ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Phantom Threat ({} rounds)".format(args.get_arg(1)))
    return 0

def phantomThreatSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("PHANTOM_THREAT"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("PHANTOM_THREAT"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def phantomThreatSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def phantomThreatSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def phantomThreatSpellSpellEnd(attachee, args, evt_obj):
    print "Phantom Threat SpellEnd"
    return 0

phantomThreatSpell = PythonModifier("sp-Phantom Threat", 2) # spell_id, duration
phantomThreatSpell.AddHook(ET_OnToHitBonusFromDefenderCondition, EK_NONE, phantomThreatSpellSetFlankedCondition,())
phantomThreatSpell.AddHook(ET_OnGetTooltip, EK_NONE, phantomThreatSpellTooltip, ())
phantomThreatSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, phantomThreatSpellEffectTooltip, ())
phantomThreatSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, phantomThreatSpellSpellEnd, ())
phantomThreatSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, phantomThreatSpellHasSpellActive, ())
phantomThreatSpell.AddHook(ET_OnD20Signal, EK_S_Killed, phantomThreatSpellKilled, ())
phantomThreatSpell.AddSpellDispelCheckStandard()
phantomThreatSpell.AddSpellTeleportPrepareStandard()
phantomThreatSpell.AddSpellTeleportReconnectStandard()
phantomThreatSpell.AddSpellCountdownStandardHook()
