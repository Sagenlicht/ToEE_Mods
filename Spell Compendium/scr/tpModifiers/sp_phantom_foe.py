from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Phantom Foe"

def phantomFoeSpellBeginRound(attachee, args, evt_obj):
    if not any(partyMember.can_melee(attachee) for partyMember in game.party):
        attachee.float_text_line("No longer threatened")
        args.set_arg(1, -1)
    return 0

def phantomFoeSpellAttackMissChance(attachee, args, evt_obj):
    evt_obj.bonus_list.add(50,0,"~Phantom Foe~[TAG_SPELLS_PHANTOM_FOE] Concealment Penalty") #Attacked Opponent gets 50% concealment due to Phantom Foe
    return 0

def phantomFoeSpellSetFlankedCondition(attachee, args, evt_obj):
    # check if cannot be flanked missing though I am unsure how uncanny dodge works and maybe I do not have to check for it anyways; needs testing
    if evt_obj.attack_packet.get_flags() & D20CAF_FLANKED:
        return 0

    flags = evt_obj.attack_packet.get_flags()
    flags |= D20CAF_FLANKED
    evt_obj.attack_packet.set_flags(flags)
    attachee.float_text_line("Phantom Foe", tf_red)
    #Unsure why flanked to hit bonus is not automatically added, not applicable for ranged attacks
    #if not evt_obj.attack_packet.get_flags() & D20CAF_RANGED: # does not work :(
    if not evt_obj.attack_packet.attacker.item_worn_at(item_wear_weapon_primary).obj_get_int(obj_f_weapon_flags) & OWF_RANGED_WEAPON: #checks if attacker mainhand weapon has range flag; this does not check for throwables,but throwables can also be use for melee
        evt_obj.bonus_list.add(2, 0, 201) #ID201 is flanked in bonus.mes
    return 0

def phantomFoeSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Phantom Foe (" + str(args.get_arg(1)) + " round)")
    else:
        evt_obj.append("Phantom Foe (" + str(args.get_arg(1)) + " rounds)")
    return 0

def phantomFoeSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("PHANTOM_FOE"), -2, " (" + str(args.get_arg(1)) + " round)")
    else:
        evt_obj.append(tpdp.hash("PHANTOM_FOE"), -2, " (" + str(args.get_arg(1)) + " rounds)")
    return 0

def phantomFoeSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def phantomFoeSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def phantomFoeSpellSpellEnd(attachee, args, evt_obj):
    print "Phantom Foe SpellEnd"
    return 0

phantomFoeSpell = PythonModifier("sp-Phantom Foe", 2) # spell_id, duration
phantomFoeSpell.AddHook(ET_OnBeginRound, EK_NONE, phantomFoeSpellBeginRound, ())
phantomFoeSpell.AddHook(ET_OnToHitBonusFromDefenderCondition, EK_NONE, phantomFoeSpellSetFlankedCondition,())
phantomFoeSpell.AddHook(ET_OnGetAttackerConcealmentMissChance, EK_NONE, phantomFoeSpellAttackMissChance,())
phantomFoeSpell.AddHook(ET_OnGetTooltip, EK_NONE, phantomFoeSpellTooltip, ())
phantomFoeSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, phantomFoeSpellEffectTooltip, ())
phantomFoeSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, phantomFoeSpellSpellEnd, ())
phantomFoeSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, phantomFoeSpellHasSpellActive, ())
phantomFoeSpell.AddHook(ET_OnD20Signal, EK_S_Killed, phantomFoeSpellKilled, ())
phantomFoeSpell.AddSpellDispelCheckStandard()
phantomFoeSpell.AddSpellTeleportPrepareStandard()
phantomFoeSpell.AddSpellTeleportReconnectStandard()
phantomFoeSpell.AddSpellCountdownStandardHook()
