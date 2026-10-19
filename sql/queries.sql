-- ====================================================================
-- Mood Tracker: SQL-запросы предметной области (ПР7)
-- ====================================================================

-- --------------------------------------------------------------------
-- 1. Выборка списков (SELECT, ORDER BY)
-- --------------------------------------------------------------------

-- Запрос 1. Список всех типов настроения с сортировкой по названию
SELECT
    id,
    name,
    description
FROM moods
ORDER BY name;

-- Запрос 2. Список всех факторов влияния с сортировкой по категории и названию
SELECT
    id,
    name,
    category
FROM factors
ORDER BY category, name;

-- --------------------------------------------------------------------
-- 2. Фильтрация данных (WHERE)
-- --------------------------------------------------------------------

-- Запрос 3. Записи с высокой оценкой настроения (оценка >= 7, хорошие дни)
SELECT
    id,
    entry_date,
    score,
    comment
FROM entries
WHERE score >= 7
ORDER BY score DESC, entry_date DESC;

-- Запрос 4. Факторы влияния определенной категории ('Здоровье')
SELECT
    id,
    name,
    category
FROM factors
WHERE category = 'Здоровье'
ORDER BY name;

-- Запрос 5. Поиск записей за конкретную дату ('2026-09-13')
SELECT
    id,
    user_id,
    mood_id,
    entry_date,
    score,
    comment
FROM entries
WHERE entry_date = '2026-09-13'
ORDER BY id;

-- --------------------------------------------------------------------
-- 3. Соединение таблиц (JOIN)
-- --------------------------------------------------------------------

-- Запрос 6. Полная информация о записях с пользователями и настроениями
SELECT
    entries.id,
    entries.entry_date,
    entries.score,
    entries.comment,
    users.name AS user_name,
    users.email AS user_email,
    moods.name AS mood_name,
    moods.description AS mood_description
FROM entries
JOIN users ON entries.user_id = users.id
LEFT JOIN moods ON entries.mood_id = moods.id
ORDER BY entries.entry_date DESC;

-- Запрос 7. Записи настроения с привязанными факторами влияния
SELECT
    entries.id AS entry_id,
    entries.entry_date,
    factors.name AS factor_name,
    factors.category AS factor_category
FROM entries
JOIN entry_factors ON entries.id = entry_factors.entry_id
JOIN factors ON entry_factors.factor_id = factors.id
ORDER BY entries.id, factors.name;

-- --------------------------------------------------------------------
-- 4. Подзапросы (NOT IN / поиск неиспользованных сущностей)
-- --------------------------------------------------------------------

-- Запрос 8. Типы настроения, не использованные в записях на выбранную дату
SELECT
    moods.id,
    moods.name,
    moods.description
FROM moods
WHERE moods.id NOT IN (
    SELECT entries.mood_id
    FROM entries
    WHERE entries.entry_date = '2026-09-13'
      AND entries.mood_id IS NOT NULL
)
ORDER BY moods.name;

-- --------------------------------------------------------------------
-- 5. Агрегатные функции (COUNT, AVG, MIN, MAX)
-- --------------------------------------------------------------------

-- Запрос 9. Общие показатели: количество записей, средняя, мин и макс оценка
SELECT
    COUNT(*) AS total_entries,
    ROUND(AVG(score), 2) AS avg_score,
    MIN(score) AS min_score,
    MAX(score) AS max_score
FROM entries;

-- Запрос 10. Количество факторов влияния по категориям
SELECT
    category,
    COUNT(*) AS factors_count
FROM factors
GROUP BY category
ORDER BY factors_count DESC, category ASC;

-- --------------------------------------------------------------------
-- 6. Группировка и фильтрация групп (GROUP BY, HAVING)
-- --------------------------------------------------------------------

-- Запрос 11. Количество записей и средняя оценка по каждому типу настроения
SELECT
    moods.id AS mood_id,
    moods.name AS mood_name,
    COUNT(entries.id) AS entries_count,
    ROUND(AVG(entries.score), 1) AS avg_score
FROM moods
LEFT JOIN entries ON moods.id = entries.mood_id
GROUP BY moods.id, moods.name
ORDER BY entries_count DESC, moods.name ASC;

-- Запрос 12. Типы настроения с количеством записей не менее 1 (HAVING)
SELECT
    moods.id AS mood_id,
    moods.name AS mood_name,
    COUNT(entries.id) AS entries_count
FROM moods
JOIN entries ON moods.id = entries.mood_id
GROUP BY moods.id, moods.name
HAVING COUNT(entries.id) >= 1
ORDER BY entries_count DESC, moods.name ASC;
