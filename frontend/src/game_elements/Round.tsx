interface RoundData {
    enemyHp: number
}

export default function Round({enemyHp}: RoundData) {

    return (
        <>
            <p>
                {enemyHp}
            </p>
        </>
    )
}