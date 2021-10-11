from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
import spell_utils
print "Registering sp-Acid Fog"

def acidFogSpellOnConditionAdd(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    acidFogPartsysId = game.particles('sp-Acid Fog', attachee)
    spellPacket.add_spell_object(attachee, acidFogPartsysId) # store the spell obj and the particle sys
    radiusAcidFog = 20.0
    acidFogEventId = attachee.object_event_append(OLC_CRITTERS, radiusAcidFog)
    args.set_arg(3, acidFogEventId)
    spellPacket.update_registry()
    return 0

def acidFogSpellOnEnteredAoe(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    spellCaster = spellPacket.caster
    spellTarget = evt_obj.target
    acidFogEventId = args.get_arg(3)

    if acidFogEventId != evt_obj.evt_id:
        return 0

    if spellPacket.add_target(spellTarget, 0):
        if spellTarget.condition_add_with_args('Acid Fog Effect', args.get_arg(0), args.get_arg(1), args.get_arg(2), args.get_arg(3)):
            spellTarget.float_text_line("Concealed")
        else:
            spellPacket.remove_target(spellTarget)
    return 0

def acidFogSpellSignalCombatEnd(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    spellTargetCount = 0
    while spellTargetCount < spellPacket.target_count:
        spellPacket.get_target(spellTargetCount).d20_send_signal(S_Spell_End, args.get_arg(0))
        spellTargetCount += 1
    args.set_arg(1, -1)
    return 0

acidFogSpell = PythonModifier("sp-Acid Fog", 4) # spell_id, duration, empty, eventId
acidFogSpell.AddHook(ET_OnConditionAdd, EK_NONE, acidFogSpellOnConditionAdd, ())
acidFogSpell.AddHook(ET_OnObjectEvent, EK_OnEnterAoE, acidFogSpellOnEnteredAoe, ())
acidFogSpell.AddHook(ET_OnD20Signal, EK_S_Combat_End, acidFogSpellSignalCombatEnd, ())
acidFogSpell.AddHook(ET_OnGetTooltip, EK_NONE, spell_utils.spellTooltip, ())
acidFogSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, spell_utils.spellEffectTooltip, ())
acidFogSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, spell_utils.queryActiveSpell, ())
acidFogSpell.AddHook(ET_OnD20Signal, EK_S_Killed, spell_utils.spellKilled, ())
acidFogSpell.AddSpellCountdownStandardHook()
acidFogSpell.AddAoESpellEndStandardHook()

#### Acid Fog Effect ####

def acidFogEffectOnBeginRound(attachee, args, evt_obj):
    args.set_arg(1, args.get_arg(1)-evt_obj.data1) # Ticking down duration
    if args.get_arg(1) < 0:
        args.condition_remove()
    else:
        spellPacket = tpdp.SpellPacket(args.get_arg(0))
        spellDamageDice = dice_new('1d6')
        spellDamageDice.number = 2
        damageType = D20DT_ACID 
        attachee.spell_damage(spellPacket.caster, damageType, spellDamageDice, D20DAP_UNSPECIFIED, D20A_CAST_SPELL, args.get_arg(0))
    return 0

def acidFogEffectSuppressFiveFoot(attachee, args, evt_obj):
    evt_obj.tb_status.flags |= TBSF_Movement
    return 0

def acidFogEffectConcealment(attachee, args, evt_obj):
    #Vanilla Solid Fog denies Concealment when attacker is under a True Seeing effect
    #I think this is wrong, True Seeing should not cancel fog effects, only "normal" concealment effects
    #While in Fog, can't be hit by ranged attacks
    #Vanilla Solid Fog handles this by reducing damage to 0
    #I am unsure why not simply raising concealment to 100
    #and not quering for anything isn't a more obvious choice?
    attacker = evt_obj.attack_packet.attacker
    #bonusValue = 50 if attacker.distance_to(attachee) > 5.0 else 20 #Acid Fog grants 20% Concealment Bonus if attacker is within 5 feet, else 50% while in Fog
    if evt_obj.attack_packet.get_flags() & D20CAF_RANGED:
        bonusValue = 100
        attachee.float_text_line("Can't be targeted by ranged attacks", tf_red)
    elif attacker.distance_to(attachee) > 5.0:
        bonusValue = 50
    else:
        bonusValue = 20
    bonusType = 19 #ID 19 = Concealment
    evt_obj.bonus_list.add(bonusValue, bonusType, "~Acid Fog~[TAG_SPELLS_ACID_FOG] Concealment Bonus")
    return 0

def acidFogEffectMovementRestriction(attachee, args, evt_obj):
    if not attachee.d20_query(Q_Critter_Has_Freedom_of_Movement):
        capValue = 5 #Acid Fog limits movement to 5 feet
        capType = 0 #ID 0 = Untyped
        bonusMesId = 258 #ID 258 = Solid Fog; would need to do create own ID for Acid Fog msg and it is not visible anyways
        evt_obj.bonus_list.set_overall_cap(1, capValue, capType, bonusMesId)
    return 0

def acidFogEffectToHitPenalty(attachee, args, evt_obj):
    bonusValue = -2 #Acid Fog gives a -2 penalty to Hit for melee attacks
    bonusType = 0 #ID 0 = Untyped (stacking)
    evt_obj.bonus_list.add(bonusValue, bonusType, "~Acid Fog~[TAG_SPELLS_ACID_FOG] Penalty")

def acidFogEffectDamagePenalty(attachee, args, evt_obj):
    bonusValue = -2 #Acid Fog gives a -2 penalty to melee damage
    bonusType = 0 #ID 0 = Untyped (stacking)
    evt_obj.damage_packet.bonus_list.add(bonusValue, bonusType, "~Acid Fog~[TAG_SPELLS_ACID_FOG] Penalty")

def acidFogEffectOnLeaveAoE(attachee, args, evt_obj):
    acidFogEventId = args.get_arg(3)
    if acidFogEventId != evt_obj.evt_id:
        return 0
    args.condition_remove()
    return 0

def acidFogEffectSignalEnd(attachee, args, evt_obj):
    args.condition_remove()
    return 0

def acidFogEffectOnRemove(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    spellPacket.remove_target(attachee)
    return 0

acidFogEffect = PythonModifier("Acid Fog Effect", 4) # spell_id, duration, empty, eventId
acidFogEffect.AddHook(ET_OnBeginRound, EK_NONE, acidFogEffectOnBeginRound, ())
acidFogEffect.AddHook(ET_OnTurnBasedStatusInit, EK_NONE, acidFogEffectSuppressFiveFoot, ())
acidFogEffect.AddHook(ET_OnGetDefenderConcealmentMissChance, EK_NONE, acidFogEffectConcealment, ())
acidFogEffect.AddHook(ET_OnGetMoveSpeed, EK_NONE, acidFogEffectMovementRestriction, ())
acidFogEffect.AddHook(ET_OnToHitBonus2, EK_NONE, acidFogEffectToHitPenalty, ())
acidFogEffect.AddHook(ET_OnDealingDamage, EK_NONE, acidFogEffectDamagePenalty, ())
acidFogEffect.AddHook(ET_OnObjectEvent, EK_OnLeaveAoE, acidFogEffectOnLeaveAoE, ())
acidFogEffect.AddHook(ET_OnD20Signal, EK_S_Spell_End, acidFogEffectSignalEnd, ())
acidFogEffect.AddHook(ET_OnConditionRemove, EK_NONE, acidFogEffectOnRemove, ())
acidFogEffect.AddHook(ET_OnGetTooltip, EK_NONE, spell_utils.spellTooltip, ())
acidFogEffect.AddHook(ET_OnGetEffectTooltip, EK_NONE, spell_utils.spellEffectTooltip, ())
acidFogEffect.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, spell_utils.queryActiveSpell, ())
acidFogEffect.AddHook(ET_OnD20Signal, EK_S_Killed, spell_utils.spellKilled, ())